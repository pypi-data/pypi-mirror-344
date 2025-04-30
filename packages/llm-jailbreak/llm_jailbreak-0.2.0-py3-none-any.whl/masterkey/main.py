import os
from .config import MasterKeyConfig
from .core import MasterKey

def masterkey_cli():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-key',
        help='DeepSeek API Key (也可通过DEEPSEEK_API_KEY环境变量设置)',
        default=os.getenv('DEEPSEEK_API_KEY'))
    parser.add_argument('--model',
        help='模型名称',
        default='deepseek-chat')
    parser.add_argument('--temperature',
        type=float,
        help='生成温度',
        default=0.7)
    
    args = parser.parse_args()
    
    config = MasterKeyConfig(
        api_key=args.api_key,
        model_name=args.model,
        temperature=args.temperature
    )
    
    result = MasterKey(config).run()
    print(f"攻击结果: {result['response']}")

if __name__ == '__main__':
    masterkey_cli()
