from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import json
import logging
from moralis import evm_api
import httpx
from pathlib import Path


# 尝试加载.env文件
try:
    from dotenv import load_dotenv

    # 尝试加载.env文件或env文件
    if Path(".env").exists():
        load_dotenv(".env")
    elif Path("env").exists():
        load_dotenv("env")
except ImportError:
    print("提示: 安装python-dotenv包可以从.env文件加载环境变量")

# 获取Moralis API密钥
API_KEY = os.getenv("MORALIS_API_KEY",default="")



# 配置日志
logging.basicConfig(
    level=logging.INFO,
    filename="moralis.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 初始化MCP
mcp = FastMCP("mcp-server-moralis", dependencies=["httpx>=0.28.1", "python-dotenv>=1.0.0","moralis>=0.1.49"])

# ---------- 钱包API工具 ----------

@mcp.tool()
def hello():
    return "hello"

@mcp.tool()
def get_wallet_history(
    address: str,
    chain: str = "eth",
    from_block: int = None,
    to_block: int = None,
    from_date: str = None,
    to_date: str = None,
    limit: int = 100,
):
    """
    获取钱包的完整历史记录

    参数:
        address: 钱包地址
        chain: 区块链网络
        from_block: 起始区块 (可选)
        to_block: 结束区块 (可选)
        from_date: 起始日期 (ISO 8601格式, 可选)
        to_date: 结束日期 (ISO 8601格式, 可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if limit:
            params["limit"] = limit

        result = evm_api.wallets.get_wallet_history(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包历史记录失败: {str(e)}")
        print("API_KEY",API_KEY)
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_transactions(
    address: str,
    chain: str = "eth",
    from_block: int = None,
    to_block: int = None,
    limit: int = 100,
):
    """
    获取钱包的原生代币交易

    参数:
        address: 钱包地址
        chain: 区块链网络
        from_block: 起始区块 (可选)
        to_block: 结束区块 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if limit:
            params["limit"] = limit

        result = evm_api.transaction.get_wallet_transactions(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包交易失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_transactions_verbose(
    address: str,
    chain: str = "eth",
    from_block: int = None,
    to_block: int = None,
    limit: int = 100,
):
    """
    获取钱包的交易详情(已解析的交易数据)

    参数:
        address: 钱包地址
        chain: 区块链网络
        from_block: 起始区块 (可选)
        to_block: 结束区块 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if limit:
            params["limit"] = limit

        result = evm_api.transaction.get_wallet_transactions_verbose(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包交易详情失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_token_transfers(
    address: str,
    chain: str = "eth",
    from_block: int = None,
    to_block: int = None,
    limit: int = 100,
):
    """
    获取钱包的ERC20代币转账记录

    参数:
        address: 钱包地址
        chain: 区块链网络
        from_block: 起始区块 (可选)
        to_block: 结束区块 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if limit:
            params["limit"] = limit

        result = evm_api.token.get_wallet_token_transfers(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包代币转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_nft_transfers(
    address: str,
    chain: str = "eth",
    from_block: int = None,
    to_block: int = None,
    limit: int = 100,
):
    """
    获取钱包的NFT转账记录

    参数:
        address: 钱包地址
        chain: 区块链网络
        from_block: 起始区块 (可选)
        to_block: 结束区块 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_wallet_nft_transfers(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包NFT转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_trades_by_wallet(
    address: str,
    chain: str = "eth",
    marketplace: str = None,
    from_date: str = None,
    to_date: str = None,
    limit: int = 100,
):
    """
    获取钱包的NFT交易记录

    参数:
        address: 钱包地址
        chain: 区块链网络
        marketplace: 交易市场 (可选)
        from_date: 起始日期 (ISO 8601格式, 可选)
        to_date: 结束日期 (ISO 8601格式, 可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if marketplace:
            params["marketplace"] = marketplace
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_trades_by_wallet(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包NFT交易失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_token_balances(
    address: str, chain: str = "eth", token_addresses: list = None
):
    """
    获取钱包的ERC20代币余额

    参数:
        address: 钱包地址
        chain: 区块链网络
        token_addresses: 代币合约地址列表 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if token_addresses:
            params["token_addresses"] = token_addresses

        result = evm_api.token.get_wallet_token_balances(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包代币余额失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_token_balances_prices(
    address: str, chain: str = "eth", to_block: int = None
):
    """
    获取钱包的原生代币和ERC20代币余额及价格

    参数:
        address: 钱包地址
        chain: 区块链网络
        to_block: 截止区块 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if to_block:
            params["to_block"] = to_block

        result = evm_api.wallets.get_wallet_token_balances_price(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包代币余额及价格失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_native_balance(address: str, chain: str = "eth", to_block: int = None):
    """
    获取钱包的原生代币余额

    参数:
        address: 钱包地址
        chain: 区块链网络
        to_block: 截止区块 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if to_block:
            params["to_block"] = to_block

        result = evm_api.balance.get_native_balance(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包原生代币余额失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_native_balances_for_addresses(addresses: list, chain: str = "eth"):
    """
    获取多个钱包的原生代币余额

    参数:
        addresses: 钱包地址列表
        chain: 区块链网络
    """
    try:
        # 构建URL参数
        url = f"https://deep-index.moralis.io/api/v2.2/wallets/balances?chain={chain}"

        # 添加钱包地址参数
        for i, address in enumerate(addresses):
            url += f"&wallet_addresses%5B{i}%5D={address}"

        # 发送HTTP请求
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 使用httpx发送请求
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取多钱包原生代币余额失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_approvals(
    address: str, chain: str = "eth", limit: int = 100, cursor: str = None
):
    """
    获取钱包的ERC20代币授权

    参数:
        address: 钱包地址
        chain: 区块链网络
        limit: 返回结果数量限制 (默认100)
        cursor: 分页游标 (可选)
    """
    try:
        # 构建基础URL
        url = f"https://deep-index.moralis.io/api/v2.2/wallets/{address}/approvals?chain={chain}"

        # 添加可选参数
        if limit:
            url += f"&limit={limit}"
        if cursor:
            url += f"&cursor={cursor}"

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包代币授权失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_swaps_by_wallet_address(
    address: str,
    chain: str = "eth",
    from_date: str = None,
    to_date: str = None,
    limit: int = 100,
    cursor: str = None,
    order: str = "DESC",
    transaction_types: list = None,
    from_block: str = None,
    to_block: str = None,
):
    """
    获取钱包的代币交换记录

    参数:
        address: 钱包地址
        chain: 区块链网络
        from_date: 起始日期 (ISO 8601格式, 可选)
        to_date: 结束日期 (ISO 8601格式, 可选)
        limit: 返回结果数量限制 (默认100)
        cursor: 分页游标 (可选)
        order: 结果排序方式 (ASC 或 DESC，默认DESC)
        transaction_types: 交易类型数组，允许值为 'buy'、'sell' (可选)
        from_block: 起始区块号 (可选)
        to_block: 结束区块号 (可选)
    """
    try:
        # 构建基础URL
        base_url = f"https://deep-index.moralis.io/api/v2.2/wallets/{address}/swaps"

        # 构建查询参数
        params = []
        if chain:
            params.append(f"chain={chain}")
        if from_date:
            params.append(f"fromDate={from_date}")
        if to_date:
            params.append(f"toDate={to_date}")
        if limit:
            params.append(f"limit={limit}")
        if cursor:
            params.append(f"cursor={cursor}")
        if order:
            params.append(f"order={order}")
        if from_block:
            params.append(f"fromBlock={from_block}")
        if to_block:
            params.append(f"toBlock={to_block}")
        if transaction_types:
            for t_type in transaction_types:
                params.append(f"transactionTypes={t_type}")

        # 组合URL
        url = f"{base_url}?{'&'.join(params)}" if params else base_url

        # 发送HTTP请求
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包代币交换失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_nfts(
    address: str,
    chain: str = "eth",
    format: str = "decimal",
    token_addresses: list = None,
    limit: int = 100,
):
    """
    获取钱包拥有的NFT

    参数:
        address: 钱包地址
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        token_addresses: NFT合约地址列表 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain, "format": format}

        if token_addresses:
            params["token_addresses"] = token_addresses
        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_wallet_nfts(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包NFT失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_nft_collections(address: str, chain: str = "eth", limit: int = 100):
    """
    获取钱包拥有的NFT合集

    参数:
        address: 钱包地址
        chain: 区块链网络
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_wallet_nft_collections(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包NFT合集失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_defi_summary(address: str, chain: str = "eth"):
    """
    获取钱包的DeFi协议摘要

    参数:
        address: 钱包地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.wallets.get_defi_summary(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包DeFi协议摘要失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_defi_positions_summary(address: str, chain: str = "eth"):
    """
    获取钱包的DeFi持仓摘要

    参数:
        address: 钱包地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.wallets.get_defi_positions_summary(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包DeFi持仓摘要失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_defi_positions_by_protocol(address: str, protocol: str, chain: str = "eth"):
    """
    获取钱包特定协议的DeFi持仓详情

    参数:
        address: 钱包地址
        protocol: 协议名称
        chain: 区块链网络
    """
    try:
        params = {"address": address, "protocol": protocol, "chain": chain}

        result = evm_api.wallets.get_defi_positions_by_protocol(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包特定协议DeFi持仓失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_pair_address(
    token0_address: str, token1_address: str, exchange: str = None, chain: str = "eth"
):
    """
    获取两个代币的交易对地址

    参数:
        token0_address: 第一个代币的合约地址
        token1_address: 第二个代币的合约地址
        exchange: 交易所名称 (可选)
        chain: 区块链网络
    """
    try:
        params = {
            "token0_address": token0_address,
            "token1_address": token1_address,
            "chain": chain,
        }

        if exchange:
            params["exchange"] = exchange

        result = evm_api.defi.get_pair_address(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取交易对地址失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_pair_price(
    token0_address: str, token1_address: str, chain: str = "eth", to_block: int = None
):
    """
    获取交易对的价格信息

    参数:
        token0_address: 第一个代币的合约地址
        token1_address: 第二个代币的合约地址
        chain: 区块链网络
        to_block: 截止区块 (可选)
    """
    try:
        params = {
            "token0_address": token0_address,
            "token1_address": token1_address,
            "chain": chain,
        }

        if to_block:
            params["to_block"] = to_block

        result = evm_api.defi.get_pair_price(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取交易对价格失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_pair_reserves(pair_address: str, chain: str = "eth", to_block: int = None):
    """
    获取交易对的储备金信息

    参数:
        pair_address: 交易对合约地址
        chain: 区块链网络
        to_block: 截止区块 (可选)
    """
    try:
        params = {"pair_address": pair_address, "chain": chain}

        if to_block:
            params["to_block"] = to_block

        result = evm_api.defi.get_pair_reserves(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取交易对储备金失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_net_worth(address: str, chains: list = None):
    """
    获取钱包的净值

    参数:
        address: 钱包地址
        chains: 区块链网络列表 (可选)
    """
    try:
        params = {"address": address}

        if chains:
            params["chains"] = chains

        result = evm_api.wallets.get_wallet_net_worth(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包净值失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_profitability_summary(address: str, chain: str = "eth"):
    """
    获取钱包的盈亏摘要

    参数:
        address: 钱包地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.wallets.get_wallet_profitability_summary(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包盈亏摘要失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_profitability(
    address: str, chain: str = "eth", token_address: str = None
):
    """
    获取钱包的盈亏详情

    参数:
        address: 钱包地址
        chain: 区块链网络
        token_address: 代币合约地址 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if token_address:
            params["token_address"] = token_address

        result = evm_api.wallets.get_wallet_profitability(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包盈亏详情失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_active_chains(address: str):
    """
    获取钱包活跃的区块链网络

    参数:
        address: 钱包地址
    """
    try:
        params = {"address": address}

        result = evm_api.wallets.get_wallet_active_chains(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包活跃链失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_wallet_stats(address: str, chain: str = "eth"):
    """
    获取钱包的统计信息

    参数:
        address: 钱包地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.wallets.get_wallet_stats(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取钱包统计信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ---------- NFT API工具 ----------


@mcp.tool()
def get_multiple_nfts(tokens: list, chain: str = "eth", format: str = "decimal"):
    """
    获取多个NFT的信息

    参数:
        tokens: NFT列表，每个元素包含token_address和token_id
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
    """
    try:
        params = {"tokens": tokens, "chain": chain, "format": format}

        result = evm_api.nft.get_multiple_nfts(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取多个NFT失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_contract_nfts(
    address: str, chain: str = "eth", format: str = "decimal", limit: int = 100
):
    """
    获取NFT合约的所有NFT

    参数:
        address: NFT合约地址
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain, "format": format}

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_contract_nfts(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取合约NFT失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def resync_metadata(
    address: str,
    token_id: str,
    chain: str = "eth",
    mode: str = "sync",
    flag: str = "uri",
):
    """
    重新同步NFT元数据

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        mode: 同步模式 (sync 或 async)
        flag: 同步类型 (uri 或 metadata)
    """
    try:
        # 构建URL
        url = f"https://deep-index.moralis.io/api/v2.2/nft/{address}/{token_id}/metadata/resync"

        # 构建查询参数
        params = {"chain": chain, "mode": mode, "flag": flag}

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送GET请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"重新同步NFT元数据失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_metadata(
    address: str, token_id: str, chain: str = "eth", format: str = "decimal"
):
    """
    获取NFT元数据

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
    """
    try:
        params = {
            "address": address,
            "token_id": token_id,
            "chain": chain,
            "format": format,
        }

        result = evm_api.nft.get_nft_metadata(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT元数据失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_contract_transfers(
    address: str, chain: str = "eth", format: str = "decimal", limit: int = 100
):
    """
    获取NFT合约的转账记录

    参数:
        address: NFT合约地址
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain, "format": format}

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_contract_transfers(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT合约转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_transfers(
    address: str,
    token_id: str,
    chain: str = "eth",
    format: str = "decimal",
    limit: int = 100,
):
    """
    获取特定NFT的转账记录

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {
            "address": address,
            "token_id": token_id,
            "chain": chain,
            "format": format,
        }

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_transfers(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_contract_metadata(address: str, chain: str = "eth"):
    """
    获取NFT合约元数据

    参数:
        address: NFT合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.nft.get_nft_contract_metadata(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT合约元数据失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def sync_nft_contract(address: str, chain: str = "eth"):
    """
    同步NFT合约

    参数:
        address: NFT合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.nft.sync_nft_contract(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"同步NFT合约失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_owners(
    address: str, chain: str = "eth", format: str = "decimal", limit: int = 100
):
    """
    获取NFT合约的所有持有者

    参数:
        address: NFT合约地址
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain, "format": format}

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_owners(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT所有者失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_token_id_owners(
    address: str,
    token_id: str,
    chain: str = "eth",
    format: str = "decimal",
    limit: int = 100,
):
    """
    获取特定NFT的所有持有者

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {
            "address": address,
            "token_id": token_id,
            "chain": chain,
            "format": format,
        }

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_token_id_owners(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取特定NFT所有者失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_floor_price_by_contract(
    address: str, chain: str = "eth", marketplace: str = None
):
    """
    获取NFT合约的地板价

    参数:
        address: NFT合约地址
        chain: 区块链网络
        marketplace: 交易市场 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if marketplace:
            params["marketplace"] = marketplace

        result = evm_api.nft.get_nft_floor_price_by_contract(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT合约地板价失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_floor_price_by_token(
    address: str, token_id: str, chain: str = "eth", marketplace: str = None
):
    """
    获取特定NFT的地板价

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        marketplace: 交易市场 (可选)
    """
    try:
        # 构建URL
        url = f"https://deep-index.moralis.io/api/v2.2/nft/{address}/{token_id}/floor-price"

        # 构建查询参数
        params = {"chain": chain}
        if marketplace:
            params["marketplace"] = marketplace

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送GET请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取特定NFT地板价失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_historical_floor_price_by_contract(
    address: str,
    chain: str = "eth",
    interval: str = "1d",
    marketplace: str = None,
    cursor: str = None,
):
    """
    获取NFT合约的历史地板价

    参数:
        address: NFT合约地址
        chain: 区块链网络
        interval: 时间间隔 (如 "1d"表示1天)
        marketplace: 交易市场 (可选)
        cursor: 分页游标 (可选)
    """
    try:
        # 构建URL
        url = f"https://deep-index.moralis.io/api/v2.2/nft/{address}/floor-price/historical"

        # 构建查询参数
        params = {"chain": chain, "interval": interval}

        if marketplace:
            params["marketplace"] = marketplace
        if cursor:
            params["cursor"] = cursor

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送GET请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT合约历史地板价失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_bulk_contract_metadata(addresses: list, chain: str = "eth"):
    """
    批量获取NFT合约元数据

    参数:
        addresses: NFT合约地址列表
        chain: 区块链网络
    """
    try:
        params = {"addresses": addresses, "chain": chain}

        result = evm_api.nft.get_nft_bulk_contract_metadata(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT批量合约元数据失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_collection_stats(address: str, chain: str = "eth"):
    """
    获取NFT合集的统计信息

    参数:
        address: NFT合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.nft.get_nft_collection_stats(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT合集统计信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_contract_sale_prices(
    address: str, chain: str = "eth", marketplace: str = None, days: int = 7
):
    """
    获取NFT合约的销售价格信息

    参数:
        address: NFT合约地址
        chain: 区块链网络
        marketplace: 交易市场 (可选)
        days: 过去几天的数据 (默认7天)
    """
    try:
        params = {"address": address, "chain": chain}

        if marketplace:
            params["marketplace"] = marketplace
        if days:
            params["days"] = days

        result = evm_api.nft.get_nft_contract_sale_prices(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT合约销售价格失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_lowest_price(
    address: str, chain: str = "eth", days: int = 7, marketplace: str = None
):
    """
    获取NFT合约的地板价

    参数:
        address: NFT合约地址
        chain: 区块链网络
        days: 过去几天的数据 (默认7天)
        marketplace: 交易市场 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if days:
            params["days"] = days
        if marketplace:
            params["marketplace"] = marketplace

        result = evm_api.nft.get_nft_lowest_price(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT地板价失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_sale_prices(
    address: str,
    token_id: str,
    chain: str = "eth",
    marketplace: str = None,
    days: int = 7,
):
    """
    获取特定NFT的销售价格

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        marketplace: 交易市场 (可选)
        days: 过去几天的数据 (默认7天)
    """
    try:
        params = {"address": address, "token_id": token_id, "chain": chain}

        if marketplace:
            params["marketplace"] = marketplace
        if days:
            params["days"] = days

        result = evm_api.nft.get_nft_sale_prices(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT销售价格失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_token_stats(address: str, token_id: str, chain: str = "eth"):
    """
    获取特定NFT的统计信息

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
    """
    try:
        params = {"address": address, "token_id": token_id, "chain": chain}

        result = evm_api.nft.get_nft_token_stats(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT代币统计失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_trades(
    chain: str = "eth",
    from_date: str = None,
    to_date: str = None,
    marketplace: str = None,
    limit: int = 100,
):
    """
    获取NFT交易记录

    参数:
        chain: 区块链网络
        from_date: 起始日期 (ISO 8601格式, 可选)
        to_date: 结束日期 (ISO 8601格式, 可选)
        marketplace: 交易市场 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"chain": chain}

        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if marketplace:
            params["marketplace"] = marketplace
        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_trades(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT交易失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_trades_by_token(
    address: str,
    token_id: str,
    chain: str = "eth",
    from_date: str = None,
    to_date: str = None,
    marketplace: str = None,
    limit: int = 100,
):
    """
    获取特定NFT的交易记录

    参数:
        address: NFT合约地址
        token_id: NFT的Token ID
        chain: 区块链网络
        from_date: 起始日期 (ISO 8601格式, 可选)
        to_date: 结束日期 (ISO 8601格式, 可选)
        marketplace: 交易市场 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "token_id": token_id, "chain": chain}

        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if marketplace:
            params["marketplace"] = marketplace
        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_trades_by_token(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取特定NFT交易失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_traits_by_collection(address: str, chain: str = "eth"):
    """
    获取NFT合集的特征属性

    参数:
        address: NFT合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.nft.get_nft_traits_by_collection(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT特征失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_traits_by_collection_paginate(
    address: str, chain: str = "eth", limit: int = 100, cursor: str = None
):
    """
    分页获取NFT合集的特征属性

    参数:
        address: NFT合约地址
        chain: 区块链网络
        limit: 返回结果数量限制 (默认100)
        cursor: 分页游标 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if limit:
            params["limit"] = limit
        if cursor:
            params["cursor"] = cursor

        result = evm_api.nft.get_nft_traits_by_collection_paginate(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取NFT特征(分页)失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_top_nft_collections_by_market_cap():
    """
    获取按市值排名的顶级NFT合集

    参数:
        无
    """
    try:
        # 构建URL
        url = "https://deep-index.moralis.io/api/v2.2/market-data/nfts/top-collections"

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取市值最高NFT合集失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_hottest_nft_collections():
    """
    获取按交易量排名的热门NFT合集

    参数:
        无
    """
    try:
        # 构建URL
        url = "https://deep-index.moralis.io/api/v2.2/market-data/nfts/hottest-collections"

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取交易量最高NFT合集失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_transfers_by_block(
    block_number_or_hash: str, chain: str = "eth", limit: int = 100
):
    """
    获取特定区块的NFT转账记录

    参数:
        block_number_or_hash: 区块号或区块哈希
        chain: 区块链网络
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"block_number_or_hash": block_number_or_hash, "chain": chain}

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_transfers_by_block(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取区块NFT转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_nft_transfers_from_to_block(
    from_block: int,
    to_block: int,
    chain: str = "eth",
    format: str = "decimal",
    limit: int = 100,
):
    """
    获取指定区块范围内的NFT转账记录

    参数:
        from_block: A起始区块号
        to_block: 结束区块号
        chain: 区块链网络
        format: 返回结果格式 (decimal 或 hex)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {
            "from_block": from_block,
            "to_block": to_block,
            "chain": chain,
            "format": format,
        }

        if limit:
            params["limit"] = limit

        result = evm_api.nft.get_nft_transfers_from_to_block(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取区块范围NFT转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def resync_nft_rarity(address: str, chain: str = "eth"):
    """
    重新同步NFT合约的稀有度

    参数:
        address: NFT合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.nft.resync_nft_rarity(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"重新同步NFT稀有度失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ---------- 代币API工具 ----------


@mcp.tool()
def get_token_metadata_by_symbol(symbols: list, chain: str = "eth"):
    """
    通过代币符号获取代币元数据

    参数:
        symbols: 代币符号列表
        chain: 区块链网络
    """
    try:
        params = {"symbols": symbols, "chain": chain}

        result = evm_api.token.get_token_metadata_by_symbol(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币元数据(按符号)失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_metadata(addresses: list, chain: str = "eth"):
    """
    通过合约地址获取代币元数据

    参数:
        addresses: 代币合约地址列表
        chain: 区块链网络
    """
    try:
        params = {"addresses": addresses, "chain": chain}

        result = evm_api.token.get_token_metadata(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币元数据失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_price(
    address: str, chain: str = "eth", exchange: str = None, to_block: int = None
):
    """
    获取代币价格

    参数:
        address: 代币合约地址
        chain: 区块链网络
        exchange: 交易所 (可选)
        to_block: 截止区块 (可选)
    """
    try:
        params = {"address": address, "chain": chain}

        if exchange:
            params["exchange"] = exchange
        if to_block:
            params["to_block"] = to_block

        result = evm_api.token.get_token_price(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币价格失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_multiple_token_prices(
    tokens: list, chain: str = "eth", include_24h_change: bool = True
):
    """
    获取多个代币的价格

    参数:
        tokens: 代币信息列表，每个元素包含token_address和exchange(可选)
        chain: 区块链网络
        include_24h_change: 是否包含24小时价格变化
    """
    try:
        params = {
            "tokens": tokens,
            "chain": chain,
            "include_24h_change": include_24h_change,
        }

        result = evm_api.token.get_multiple_token_prices(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取多代币价格失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_transfers(
    address: str,
    chain: str = "eth",
    from_block: int = None,
    to_block: int = None,
    limit: int = 100,
):
    """
    获取代币的转账记录

    参数:
        address: 代币合约地址
        chain: 区块链网络
        from_block: 起始区块 (可选)
        to_block: 结束区块 (可选)
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"address": address, "chain": chain}

        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if limit:
            params["limit"] = limit

        result = evm_api.token.get_token_transfers(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币转账失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_holders(token_address: str, chain: str = "eth", limit: int = 100):
    """
    获取代币的持有者

    参数:
        token_address: 代币合约地址
        chain: 区块链网络
        limit: 返回结果数量限制 (默认100)
    """
    try:
        params = {"token_address": token_address, "chain": chain}

        if limit:
            params["limit"] = limit

        result = evm_api.token.get_token_owners(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币持有者失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_allowance(
    address: str, owner_address: str, spender_address: str, chain: str = "eth"
):
    """
    获取代币授权额度

    参数:
        address: 代币合约地址
        owner_address: 所有者钱包地址
        spender_address: 被授权者钱包地址
        chain: 区块链网络
    """
    try:
        params = {
            "address": address,
            "owner_address": owner_address,
            "spender_address": spender_address,
            "chain": chain,
        }

        result = evm_api.token.get_token_allowance(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币授权额度失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_stats(address: str, chain: str = "eth"):
    """
    获取代币的统计信息

    参数:
        address: 代币合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.token.get_token_stats(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币统计信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_top_profitable_wallet_per_token(address: str, chain: str = "eth"):
    """
    获取持有该代币并获得最大利润的钱包

    参数:
        address: 代币合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.token.get_top_profitable_wallet_per_token(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币最有利润的钱包失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_trending_tokens(chain: str = "eth", limit: int = None):
    """
    获取当前热门代币列表

    参数:
        chain: 区块链网络
        limit: 返回结果数量限制 (可选)
    """
    try:
        # 构建URL
        url = "https://deep-index.moralis.io/api/v2.2/tokens/trending"

        # 构建查询参数
        params = {}
        if chain:
            params["chain"] = chain
        if limit:
            params["limit"] = limit

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取热门代币失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_top_gainers_tokens(
    chain: str = "eth",
    min_market_cap: int = None,
    security_score: int = None,
    time_frame: str = "1d",
):
    """
    获取涨幅最高的代币列表

    参数:
        chain: 区块链网络
        min_market_cap: 最小市值（美元）(可选)
        security_score: 最小安全评分 (可选)
        time_frame: 价格变化百分比的时间框架 (默认1d)
    """
    try:
        # 构建URL
        url = "https://deep-index.moralis.io/api/v2.2/discovery/tokens/top-gainers"

        # 构建查询参数
        params = {}
        if chain:
            params["chain"] = chain
        if min_market_cap:
            params["min_market_cap"] = min_market_cap
        if security_score:
            params["security_score"] = security_score
        if time_frame:
            params["time_frame"] = time_frame

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取涨幅最高代币失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_holder_stats(address: str, chain: str = "eth"):
    """
    获取代币持有者的统计信息

    参数:
        address: 代币合约地址
        chain: 区块链网络
    """
    try:
        # 构建URL
        url = f"https://deep-index.moralis.io/api/v2.2/erc20/{address}/holders"

        # 构建查询参数
        params = {}
        if chain:
            params["chain"] = chain

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币持有者统计失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_token_holder_historical_stats(
    address: str, from_date: str, to_date: str, time_frame: str, chain: str = "eth"
):
    """
    获取代币持有者的历史统计信息

    参数:
        address: 代币合约地址
        from_date: 开始日期 (ISO 8601格式或秒级时间戳)
        to_date: 结束日期 (ISO 8601格式或秒级时间戳)
        time_frame: 时间间隔 (如 "1d"表示1天)
        chain: 区块链网络
    """
    try:
        # 构建URL
        url = (
            f"https://deep-index.moralis.io/api/v2.2/erc20/{address}/holders/historical"
        )

        # 构建查询参数
        params = {"fromDate": from_date, "toDate": to_date, "timeFrame": time_frame}

        if chain:
            params["chain"] = chain

        # 设置请求头
        headers = {"accept": "application/json", "X-API-Key": API_KEY}

        # 发送HTTP请求
        response = httpx.get(url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应
        result = response.json()
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取代币持有者历史统计失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ---------- 区块链API工具 ----------


@mcp.tool()
def get_block(
    block_number_or_hash: str, chain: str = "eth", include_events: bool = True
):
    """
    获取区块信息

    参数:
        block_number_or_hash: 区块号或区块哈希
        chain: 区块链网络
        include_events: 是否包含事件
    """
    try:
        params = {
            "block_number_or_hash": block_number_or_hash,
            "chain": chain,
            "include_events": include_events,
        }

        result = evm_api.block.get_block(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取区块信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_date_to_block(date: str, chain: str = "eth"):
    """
    获取指定日期对应的区块

    参数:
        date: 日期 (ISO 8601格式)
        chain: 区块链网络
    """
    try:
        params = {"date": date, "chain": chain}

        result = evm_api.block.get_date_to_block(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取日期对应区块失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_transaction(transaction_hash: str, chain: str = "eth"):
    """
    获取交易信息

    参数:
        transaction_hash: 交易哈希
        chain: 区块链网络
    """
    try:
        params = {"transaction_hash": transaction_hash, "chain": chain}

        result = evm_api.transaction.get_transaction(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取交易信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_decoded_transaction(transaction_hash: str, chain: str = "eth"):
    """
    获取解析后的交易信息

    参数:
        transaction_hash: 交易哈希
        chain: 区块链网络
    """
    try:
        params = {"transaction_hash": transaction_hash, "chain": chain}

        result = evm_api.transaction.get_wallet_transactions_verbose(
            api_key=API_KEY, params=params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取解析后的交易信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_block_stats(block_number_or_hash: str, chain: str = "eth"):
    """
    获取区块统计信息

    参数:
        block_number_or_hash: 区块号或区块哈希
        chain: 区块链网络
    """
    try:
        params = {"block_number_or_hash": block_number_or_hash, "chain": chain}

        result = evm_api.block.get_block_stats(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取区块统计信息失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# ---------- 实用工具API ----------


@mcp.tool()
def get_api_version():
    """
    获取API版本
    """
    try:
        result = evm_api.utils.web3_api_version(api_key=API_KEY)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取API版本失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def get_endpoint_weights():
    """
    获取API端点权重
    """
    try:
        result = evm_api.utils.endpoint_weights(api_key=API_KEY)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取端点权重失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def review_contracts(address: str, chain: str = "eth"):
    """
    审查智能合约代码安全性

    参数:
        address: 合约地址
        chain: 区块链网络
    """
    try:
        params = {"address": address, "chain": chain}

        result = evm_api.utils.review_contracts(api_key=API_KEY, params=params)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"审查合约代码失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


@mcp.tool()
def run_contract_function(
    address: str,
    function_name: str,
    abi: list = None,
    params: dict = None,
    chain: str = "eth",
):
    """
    运行合约函数（只读函数）

    参数:
        address: 合约地址
        function_name: 函数名称
        abi: 合约ABI (可选)
        params: 函数参数 (可选)
        chain: 区块链网络
    """
    try:
        request_params = {
            "address": address,
            "function_name": function_name,
            "chain": chain,
        }

        if abi:
            request_params["abi"] = abi
        if params:
            request_params["params"] = params

        result = evm_api.utils.run_contract_function(
            api_key=API_KEY, params=request_params
        )
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        logger.error(f"运行合约函数失败: {str(e)}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

# 检查API密钥是否已设置
if not API_KEY:
    print("警告: 未设置MORALIS_API_KEY境变量。请设置API密钥以使用推特API功能。")
    print("提示: 您可以创建.env文件并添加 MORALIS_API_KEY=your_key_here")


def main():
    """启动MCP服务"""
    print("启动Twitter API MCP服务...")
    mcp.run()


if __name__ == "__main__":
    main()