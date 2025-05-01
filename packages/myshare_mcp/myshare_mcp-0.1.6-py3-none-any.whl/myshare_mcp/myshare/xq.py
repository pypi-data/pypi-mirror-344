def get_xq_symbol(stock_code):
    """
    将股票代码转换为雪球 API 的格式。

    参数:
        stock_code (str): 股票代码，例如 '600325'。

    返回:
        str: 符合雪球 API 格式的股票代码，例如 'SH600325'。
    """
    # 确保输入是字符串类型
    stock_code = str(stock_code).strip()
    
    # 检查股票代码长度是否为 6 位
    if len(stock_code) != 6 or not stock_code.isdigit():
        raise ValueError(f"无效的股票代码：{stock_code}。股票代码必须是 6 位数字。")
    
    # 判断交易所前缀
    if stock_code.startswith("6"):
        prefix = "SH"  # 上海证券交易所
    else:
        prefix = "SZ"  # 深圳证券交易所
    
    # 拼接并返回雪球 API 格式
    return f"{prefix}{stock_code}"

# 示例调用
if __name__ == "__main__":
    # 输入股票代码
    examples = ["600325", "000001", "300059"]
    
    for example in examples:
        xueqiu_code = get_xq_symbol(example)
        print(f"股票代码 {example} 转换为雪球 API 格式: {xueqiu_code}")