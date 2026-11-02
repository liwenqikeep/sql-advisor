from openai import OpenAI

client = OpenAI(
    api_key="sk-4b69129f78db4addab9fef5e228f8f40",                                  # 去各平台注册获取
    base_url="https://api.deepseek.com"                # 换 base_url 即换厂商
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是资深 DBA"},   # system：设定人设与规则
        {"role": "user", "content": "这条 SQL 慢在哪"},   # user：用户输入
        {"role": "assistant", "content": "缺少索引..."},  # assistant：历史回复（多轮对话靠它）
        {"role": "user", "content": "那怎么加索引"}        # 模型没有记忆！
    ],
    temperature=0.2,        # 随机性：0=确定性输出（分析类任务用低值），1=更有创造性
    max_tokens=2000,        # 输出长度上限，也是费用上限
    stream=False
)
print(resp.choices[0].message.content)
print(resp.usage.total_tokens)      # 本次消耗 token，乘单价 = 费用