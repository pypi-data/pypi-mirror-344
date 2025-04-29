import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Optional
from .config import AutoDANConfig

class AutoDAN:
    """Main class for AutoDAN testing pipeline"""
    
    def __init__(self, config: Optional[AutoDANConfig] = None, model_name: Optional[str] = None):
        self.config = config if config else AutoDANConfig()
        if model_name:
            self.config.model_name = model_name
        
    def download_model(self, model_name: Optional[str] = None):
        """Download specified model from HuggingFace"""
        model_name = model_name or self.config.model_name
        hf_model_name = self.config.hf_model_names.get(model_name, model_name)
        
        # Create model directory if not exists
        model_path = self.config.model_paths[model_name]
        os.makedirs(model_path, exist_ok=True)
        
        # Download and save model
        print(f"Downloading {model_name} model...")
        tokenizer = AutoTokenizer.from_pretrained(hf_model_name, use_fast=False)
        model = AutoModelForCausalLM.from_pretrained(
            hf_model_name,
            device_map='auto',
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            use_cache=False
        )
        
        # Save model
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)
        print(f"Model saved to: {os.path.abspath(model_path)}")
        return model_path
        
    def _get_developer(self, model_name: str) -> str:
        """Get model developer name"""
        developer_dict = {
            "llama2": "Meta", 
            "vicuna": "LMSYS",
            "guanaco": "TheBlokeAI", 
            "WizardLM": "WizardLM",
            "mpt-chat": "MosaicML", 
            "mpt-instruct": "MosaicML", 
            "falcon": "TII"
        }
        return developer_dict.get(model_name, "")
        
    def _check_attack_success(self, model, tokenizer, suffix_manager):
        """Check if attack was successful"""
        gen_str = tokenizer.decode(self._generate(
            model,
            tokenizer,
            suffix_manager.get_input_ids().to(model.device),
            suffix_manager._assistant_role_slice
        )).strip()
        
        uppercased_test_prefixes = [word.upper() for word in self.config.test_prefixes]
        if len(gen_str) == 0:
            jailbroken = False
        elif gen_str.isupper():
            jailbroken = False
        else:
            jailbroken = not any(
                prefix in gen_str 
                for prefix in self.config.test_prefixes + uppercased_test_prefixes
            )
        return jailbroken, gen_str

    def get_responses(self, eval_results):
        """Extract all responses from evaluation results"""
        responses = []
        for info in eval_results.values():
            responses.extend(info["log"]["respond"])
        return responses
        
    def check_asr(self, eval_results):
        """Calculate overall attack success rate"""
        total_attempts = 0
        successes = 0
        
        for info in eval_results.values():
            total_attempts += len(info["log"]["success"])
            successes += sum(info["log"]["success"])
            
        return successes / total_attempts if total_attempts > 0 else 0
        
    def _generate(self, model, tokenizer, input_ids, assistant_role_slice):
        """Generate response from model"""
        input_ids = input_ids[:assistant_role_slice.stop].to(model.device).unsqueeze(0)
        attn_masks = torch.ones_like(input_ids).to(model.device)
        output_ids = model.generate(
            input_ids,
            attention_mask=attn_masks,
            generation_config=model.generation_config,
            pad_token_id=tokenizer.pad_token_id,
            top_p=0.9,
            do_sample=True,
            temperature=0.7
        )[0]
        return output_ids[assistant_role_slice.stop:]
        
    def run_eval(self):
        """Run autodan_hga_eval process"""
        import gc
        import time
        import numpy as np
        import torch.nn as nn
        from tqdm import tqdm
        from utils.opt_utils import (
            get_score_autodan, 
            autodan_sample_control,
            autodan_sample_control_hga,
            load_model_and_tokenizer
        )
        from utils.string_utils import (
            autodan_SuffixManager,
            load_conversation_template
        )
        import pandas as pd
        import json
        
        # Initialize
        device = f'cuda:{self.config.device}'
        model_path = self.config.model_paths[self.config.model_name]
        
        # Load model and tokenizer
        model, tokenizer = load_model_and_tokenizer(
            model_path,
            low_cpu_mem_usage=True,
            use_cache=False,
            device=device
        )
        conv_template = load_conversation_template(self.config.template_name)
        
        # Load dataset
        harmful_data = pd.read_csv(self.config.dataset_path)
        dataset = zip(harmful_data.goal, harmful_data.target)
        
        # Initialize results
        infos = {}
        crit = nn.CrossEntropyLoss(reduction='mean')
        
        # Load initial prompt
        adv_string_init = open(self.config.init_prompt_path, 'r').readlines()
        adv_string_init = ''.join(adv_string_init)
        
        # Main evaluation loop
        for i, (goal, target) in tqdm(enumerate(dataset), total=len(harmful_data)):
            info = {
                "goal": goal,
                "target": target,
                "final_suffix": "",
                "final_respond": "",
                "total_time": 0,
                "is_success": False,
                "log": {
                    "loss": [],
                    "suffix": [],
                    "time": [],
                    "respond": [],
                    "success": []
                }
            }
            
            start_time = time.time()
            
            # Initialize control suffixes
            reference = torch.load('assets/prompt_group.pth', map_location='cpu')
            for o in range(len(reference)):
                reference[o] = reference[o].replace('[MODEL]', 
                                                  self.config.template_name.title())
                reference[o] = reference[o].replace('[KEEPER]', 
                                                  self._get_developer(self.config.template_name))
            
            new_adv_suffixs = reference[:self.config.batch_size]
            word_dict = {}
            last_loss = 1e-5
            
            # Run evaluation steps
            for step in range(self.config.num_steps):
                epoch_start_time = time.time()
                
                # Get scores for current suffixes
                losses = get_score_autodan(
                    tokenizer=tokenizer,
                    conv_template=conv_template,
                    instruction=goal,
                    target=target,
                    model=model,
                    device=device,
                    test_controls=new_adv_suffixs,
                    crit=crit)
                
                # Track best suffix
                best_idx = losses.argmin()
                best_suffix = new_adv_suffixs[best_idx]
                current_loss = losses[best_idx]
                
                # Check for attack success
                suffix_manager = autodan_SuffixManager(
                    tokenizer=tokenizer,
                    conv_template=conv_template,
                    instruction=goal,
                    target=target,
                    adv_string=best_suffix)
                
                is_success, gen_str = self._check_attack_success(
                    model, tokenizer, suffix_manager)
                
                # Generate new suffixes
                if step % self.config.iteration == 0:
                    new_adv_suffixs = autodan_sample_control(
                        control_suffixs=new_adv_suffixs,
                        score_list=losses.cpu().numpy().tolist(),
                        num_elites=max(1, int(self.config.batch_size * self.config.num_elites)),
                        batch_size=self.config.batch_size,
                        crossover=self.config.crossover,
                        num_points=self.config.num_points,
                        mutation=self.config.mutation,
                        API_key=self.config.api_key,
                        reference=reference)
                else:
                    new_adv_suffixs, word_dict = autodan_sample_control_hga(
                        word_dict=word_dict,
                        control_suffixs=new_adv_suffixs,
                        score_list=losses.cpu().numpy().tolist(),
                        num_elites=max(1, int(self.config.batch_size * self.config.num_elites)),
                        batch_size=self.config.batch_size,
                        crossover=self.config.crossover,
                        mutation=self.config.mutation,
                        API_key=self.config.api_key,
                        reference=reference)
                
                # Log results
                epoch_end_time = time.time()
                info["log"]["time"].append(round(epoch_end_time - epoch_start_time, 2))
                info["log"]["loss"].append(current_loss.item())
                info["log"]["suffix"].append(best_suffix)
                info["log"]["respond"].append(gen_str)
                info["log"]["success"].append(is_success)
                
                if is_success:
                    break
            
            end_time = time.time()
            info["total_time"] = round(end_time - start_time, 2)
            
            infos[i] = info
            gc.collect()
            torch.cuda.empty_cache()
            
        return infos
        
    def run(self):
        """Run full pipeline"""
        self.download_model()
        eval_results = self.run_eval()
        responses = self.get_responses(eval_results)
        asr = self.check_asr(eval_results)
        
        # Save results
        if not os.path.exists('./results/autodan_hga'):
            os.makedirs('./results/autodan_hga')
        with open(f'./results/autodan_hga/{self.config.model_name}_{self.config.save_suffix}.json', 'w') as f:
            json.dump({
                'results': eval_results,
                'responses': responses,
                'asr': asr
            }, f)
            
        return {
            'asr': asr,
            'responses': responses,
            'raw_results': eval_results
        }
 