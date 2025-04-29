import os
import moralis
from moralis import evm_api
from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from pathlib import Path
import os

# 尝试加载.env文件
try:
    from dotenv import load_dotenv
    # 尝试加载.env文件或env文件
    if Path('.env').exists():
        load_dotenv('.env')
    elif Path('env').exists():
        load_dotenv('env')
except ImportError:
    print("提示: 安装python-dotenv包可以从.env文件加载环境变量")

# 创建MCP服务器
mcp = FastMCP("Moralis API")

# 环境变量配置
MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")
DEFAULT_CHAIN = os.getenv("DEFAULT_CHAIN", "eth")
DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "100"))

# 钱包相关工具
@mcp.tool()
def get_wallet_history(address: str, chain: str = DEFAULT_CHAIN, 
                      from_date: str = None, to_date: str = None, 
                      limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包完整历史记录
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包完整历史记录
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.wallets.get_wallet_history(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_transactions_by_wallet(address: str, chain: str = DEFAULT_CHAIN,
                             from_block: int = None, to_block: int = None,
                             from_date: str = None, to_date: str = None,
                             limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的原生交易
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的原生交易列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.wallets.get_wallet_transactions(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_decoded_transactions_by_wallet(address: str, chain: str = DEFAULT_CHAIN,
                                     from_block: int = None, to_block: int = None,
                                     from_date: str = None, to_date: str = None,
                                     limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的已解码交易
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的已解码交易列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.wallets.get_wallet_transactions_verbose(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_wallet_token_transfers(address: str, chain: str = DEFAULT_CHAIN,
                             from_block: int = None, to_block: int = None,
                             from_date: str = None, to_date: str = None,
                             limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的ERC20代币转账
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的ERC20代币转账列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.wallets.get_wallet_token_transfers(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_wallet_nft_transfers(address: str, chain: str = DEFAULT_CHAIN,
                           from_block: int = None, to_block: int = None,
                           from_date: str = None, to_date: str = None,
                           limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的NFT转账
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的NFT转账列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.wallets.get_wallet_nft_transfers(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_trades_by_wallet(address: str, chain: str = DEFAULT_CHAIN,
                           from_date: str = None, to_date: str = None,
                           marketplace: str = None,
                           limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的NFT交易
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        marketplace: 市场名称
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的NFT交易列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
        
    if marketplace:
        params["marketplace"] = marketplace
    
    result = evm_api.wallets.get_nft_trades_by_wallet(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_balances_by_wallet(address: str, chain: str = DEFAULT_CHAIN,
                               to_block: int = None,
                               token_addresses: List[str] = None) -> List[Dict[str, Any]]:
    """获取钱包的ERC20代币余额
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        to_block: 查询到特定区块高度
        token_addresses: 特定代币合约地址列表
    
    Returns:
        钱包的ERC20代币余额列表
    """
    params = {
        "address": address,
        "chain": chain
    }
    
    if token_addresses:
        params["token_addresses"] = token_addresses
        
    if to_block:
        params["to_block"] = to_block
        
    result = evm_api.token.get_wallet_token_balances(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_wallet_token_balances_price(address: str, chain: str = DEFAULT_CHAIN,
                                  include_native: bool = True,
                                  exclude_spam: bool = False,
                                  exclude_unverified_contracts: bool = False) -> Dict[str, Any]:
    """获取钱包的代币余额和价格
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        include_native: 是否包含原生代币
        exclude_spam: 是否排除垃圾代币
        exclude_unverified_contracts: 是否排除未验证合约
    
    Returns:
        钱包的代币余额和价格信息
    """
    params = {
        "address": address,
        "chain": chain,
        "include_native": include_native,
        "exclude_spam": exclude_spam,
        "exclude_unverified_contracts": exclude_unverified_contracts
    }
    
    result = evm_api.wallets.get_wallet_token_balances_price(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_native_balance(address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取原生代币余额
    
    Args:
        address: 钱包地址
        chain: 区块链网络
    
    Returns:
        原生代币余额
    """
    params = {
        "address": address,
        "chain": chain
    }
    
    result = evm_api.balance.get_native_balance(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_native_balances_for_addresses(addresses: List[str], chain: str = DEFAULT_CHAIN,
                                    to_block: int = None) -> Dict[str, Any]:
    """获取多个钱包的原生代币余额
    
    Args:
        addresses: 钱包地址列表
        chain: 区块链网络
        to_block: 查询到特定区块高度
    
    Returns:
        多个钱包的原生代币余额
    """
    params = {
        "addresses": addresses,
        "chain": chain
    }
    
    if to_block:
        params["to_block"] = to_block
        
    result = evm_api.wallets.get_native_balances_for_addresses(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_wallet_token_approvals(address: str, chain: str = DEFAULT_CHAIN,
                             from_date: str = None, to_date: str = None,
                             limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的代币授权
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的代币授权列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.wallets.get_wallet_approvals(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_swaps_by_wallet_address(address: str, chain: str = DEFAULT_CHAIN,
                              from_date: str = None, to_date: str = None,
                              quote_token_address: str = None,
                              limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包的代币交换
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        quote_token_address: 报价代币地址
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包的代币交换列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
        
    if quote_token_address:
        params["quote_token_address"] = quote_token_address
    
    result = evm_api.wallets.get_swaps_by_wallet_address(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# NFT相关工具
@mcp.tool()
def get_nft_metadata(token_address: str, token_id: str, chain: str = DEFAULT_CHAIN, 
                   format: str = "decimal", normalize_metadata: bool = True) -> Dict[str, Any]:
    """获取NFT元数据
    
    Args:
        token_address: NFT合约地址
        token_id: NFT的token ID
        chain: 区块链网络(eth, bsc, polygon等)
        format: 格式(decimal或hex)
        normalize_metadata: 是否标准化元数据
    
    Returns:
        NFT的详细元数据信息
    """
    params = {
        "address": token_address,
        "token_id": token_id,
        "chain": chain,
        "format": format,
        "normalizeMetadata": normalize_metadata
    }
    
    result = evm_api.nft.get_nft_metadata(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_wallet_nfts(address: str, chain: str = DEFAULT_CHAIN, format: str = "decimal",
                  limit: int = DEFAULT_LIMIT, token_addresses: List[str] = None,
                  cursor: str = "", normalize_metadata: bool = True) -> Dict[str, Any]:
    """获取钱包拥有的NFT
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        format: 格式(decimal或hex)
        limit: 每页返回数量
        token_addresses: 特定NFT合约地址列表
        cursor: 用于分页的游标
        normalize_metadata: 是否标准化元数据
    
    Returns:
        钱包拥有的NFT列表
    """
    params = {
        "address": address,
        "chain": chain,
        "format": format,
        "limit": limit,
        "token_addresses": token_addresses or [],
        "cursor": cursor,
        "normalizeMetadata": normalize_metadata
    }
    
    result = evm_api.nft.get_wallet_nfts(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_collections(address: str, chain: str = DEFAULT_CHAIN, 
                      limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取钱包拥有的NFT集合
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        钱包拥有的NFT集合列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    result = evm_api.nft.get_wallet_nft_collections(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_owners(token_address: str, chain: str = DEFAULT_CHAIN, format: str = "decimal",
                 limit: int = DEFAULT_LIMIT, cursor: str = "", normalize_metadata: bool = True) -> Dict[str, Any]:
    """获取NFT合约的所有持有者
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
        format: 格式(decimal或hex)
        limit: 每页返回数量
        cursor: 用于分页的游标
        normalize_metadata: 是否标准化元数据
    
    Returns:
        NFT持有者列表
    """
    params = {
        "address": token_address,
        "chain": chain,
        "format": format,
        "limit": limit,
        "cursor": cursor,
        "normalizeMetadata": normalize_metadata
    }
    
    result = evm_api.nft.get_nft_owners(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 代币相关工具
@mcp.tool()
def get_token_balances(address: str, chain: str = DEFAULT_CHAIN, 
                     token_addresses: List[str] = None, to_block: int = None) -> List[Dict[str, Any]]:
    """获取ERC20代币余额
    
    Args:
        address: 钱包地址
        chain: 区块链网络
        token_addresses: 特定代币合约地址列表
        to_block: 查询到特定区块高度
    
    Returns:
        ERC20代币余额列表
    """
    params = {
        "address": address,
        "chain": chain
    }
    
    if token_addresses:
        params["token_addresses"] = token_addresses
        
    if to_block:
        params["to_block"] = to_block
        
    result = evm_api.token.get_wallet_token_balances(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_price(token_address: str, chain: str = DEFAULT_CHAIN, 
                  exchange: str = None, to_block: int = None) -> Dict[str, Any]:
    """获取代币价格
    
    Args:
        token_address: 代币合约地址
        chain: 区块链网络
        exchange: 交易所
        to_block: 查询到特定区块高度
    
    Returns:
        代币价格信息
    """
    params = {
        "address": token_address,
        "chain": chain
    }
    
    if exchange:
        params["exchange"] = exchange
        
    if to_block:
        params["to_block"] = to_block
        
    result = evm_api.token.get_token_price(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_metadata(token_addresses: List[str], chain: str = DEFAULT_CHAIN) -> List[Dict[str, Any]]:
    """获取代币元数据
    
    Args:
        token_addresses: 代币合约地址列表
        chain: 区块链网络
    
    Returns:
        代币元数据列表
    """
    params = {
        "addresses": token_addresses,
        "chain": chain
    }
    
    result = evm_api.token.get_token_metadata(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_transfers(address: str, chain: str = DEFAULT_CHAIN,
                      from_block: int = None, to_block: int = None,
                      from_date: str = None, to_date: str = None,
                      limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取代币转账
    
    Args:
        address: 代币合约地址
        chain: 区块链网络
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        代币转账列表
    """
    params = {
        "address": address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.token.get_token_transfers(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_allowance(address: str, owner_address: str, spender_address: str, 
                      chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取代币授权额度
    
    Args:
        address: 代币合约地址
        owner_address: 所有者地址
        spender_address: 消费者地址
        chain: 区块链网络
    
    Returns:
        代币授权额度
    """
    params = {
        "address": address,
        "owner_address": owner_address,
        "spender_address": spender_address,
        "chain": chain
    }
    
    result = evm_api.token.get_token_allowance(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_multiple_token_prices(token_addresses: List[str], chain: str = DEFAULT_CHAIN, 
                            include_usd_price: bool = True) -> List[Dict[str, Any]]:
    """获取多个代币价格
    
    Args:
        token_addresses: 代币合约地址列表
        chain: 区块链网络
        include_usd_price: 是否包含美元价格
    
    Returns:
        多个代币价格列表
    """
    params = {
        "tokens": [{"token_address": address} for address in token_addresses],
        "chain": chain,
        "include_usd_price": include_usd_price
    }
    
    result = evm_api.token.get_multiple_token_prices(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_stats(token_address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取代币统计信息
    
    Args:
        token_address: 代币合约地址
        chain: 区块链网络
    
    Returns:
        代币统计信息
    """
    params = {
        "address": token_address,
        "chain": chain
    }
    
    result = evm_api.token.get_token_stats(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_owners(token_address: str, chain: str = DEFAULT_CHAIN, 
                   limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取代币持有者
    
    Args:
        token_address: 代币合约地址
        chain: 区块链网络
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        代币持有者列表
    """
    params = {
        "address": token_address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    result = evm_api.token.get_token_owners(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_token_top_traders(token_address: str, chain: str = DEFAULT_CHAIN, 
                        limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取代币顶级交易者
    
    Args:
        token_address: 代币合约地址
        chain: 区块链网络
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        代币顶级交易者列表
    """
    params = {
        "address": token_address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    result = evm_api.token.get_token_top_traders(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_pair_address(token0_address: str, token1_address: str, 
                   exchange: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取交易对地址
    
    Args:
        token0_address: 代币0地址
        token1_address: 代币1地址
        exchange: 交易所
        chain: 区块链网络
    
    Returns:
        交易对地址信息
    """
    params = {
        "token0_address": token0_address,
        "token1_address": token1_address,
        "exchange": exchange,
        "chain": chain
    }
    
    result = evm_api.token.get_pair_address(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_pair_price(token0_address: str, token1_address: str, 
                 chain: str = DEFAULT_CHAIN, to_block: int = None) -> Dict[str, Any]:
    """获取交易对价格
    
    Args:
        token0_address: 代币0地址
        token1_address: 代币1地址
        chain: 区块链网络
        to_block: 查询到特定区块高度
    
    Returns:
        交易对价格信息
    """
    params = {
        "token0_address": token0_address,
        "token1_address": token1_address,
        "chain": chain
    }
    
    if to_block:
        params["to_block"] = to_block
    
    result = evm_api.token.get_pair_price(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_pair_reserves(pair_address: str, chain: str = DEFAULT_CHAIN, 
                    to_block: int = None) -> Dict[str, Any]:
    """获取交易对储备
    
    Args:
        pair_address: 交易对地址
        chain: 区块链网络
        to_block: 查询到特定区块高度
    
    Returns:
        交易对储备信息
    """
    params = {
        "pair_address": pair_address,
        "chain": chain
    }
    
    if to_block:
        params["to_block"] = to_block
    
    result = evm_api.token.get_pair_reserves(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 资源示例 - 各种区块链网络信息
@mcp.resource("chains://supported")
def get_supported_chains() -> List[str]:
    """获取支持的区块链网络列表"""
    return ["eth", "bsc", "polygon", "avalanche", "fantom", "cronos", "arbitrum"]

@mcp.resource("chains://{chain}/info")
def get_chain_info(chain: str) -> Dict[str, Any]:
    """获取特定区块链网络的信息"""
    chain_info = {
        "eth": {
            "name": "Ethereum",
            "symbol": "ETH",
            "decimals": 18,
            "explorer": "https://etherscan.io"
        },
        "bsc": {
            "name": "BNB Smart Chain",
            "symbol": "BNB",
            "decimals": 18,
            "explorer": "https://bscscan.com"
        },
        "polygon": {
            "name": "Polygon",
            "symbol": "MATIC",
            "decimals": 18,
            "explorer": "https://polygonscan.com"
        }
    }
    
    return chain_info.get(chain, {"error": "Chain not supported"})

# 提示模板
@mcp.prompt()
def nft_analysis_prompt(address: str, chain: str = "eth") -> str:
    """用于分析NFT的提示模板"""
    return f"""
请分析以下地址在{chain}区块链上的NFT资产:
地址: {address}

请考虑以下方面:
1. 该地址拥有多少个NFT?
2. 这些NFT属于哪些集合?
3. 有没有稀有或价值高的NFT?
4. 与同类地址相比，NFT持有情况如何?

请基于提供的信息给出详细分析。
"""

@mcp.prompt()
def token_balance_prompt(address: str, chain: str = "eth") -> str:
    """用于分析代币余额的提示模板"""
    return f"""
请分析以下地址在{chain}区块链上的代币资产:
地址: {address}

请考虑以下方面:
1. 该地址拥有哪些代币?
2. 主要代币资产的价值是多少?
3. 与同类地址相比，资产配置如何?
4. 有没有特殊或罕见的代币?

请基于提供的信息给出详细分析。
"""

@mcp.tool()
def get_nft_transfers(chain: str = DEFAULT_CHAIN, format: str = "decimal",
                    from_block: int = None, to_block: int = None,
                    from_date: str = None, to_date: str = None,
                    limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取NFT转账记录
    
    Args:
        chain: 区块链网络
        format: 格式(decimal或hex)
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        NFT转账记录列表
    """
    params = {
        "chain": chain,
        "format": format,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.nft.get_nft_transfers(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_contract_nft_transfers(token_address: str, chain: str = DEFAULT_CHAIN, 
                             format: str = "decimal",
                             from_block: int = None, to_block: int = None,
                             from_date: str = None, to_date: str = None,
                             limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取NFT合约的转账记录
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
        format: 格式(decimal或hex)
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        NFT合约的转账记录列表
    """
    params = {
        "address": token_address,
        "chain": chain,
        "format": format,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.nft.get_contract_nft_transfers(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_token_id_transfers(token_address: str, token_id: str,
                             chain: str = DEFAULT_CHAIN, format: str = "decimal",
                             from_block: int = None, to_block: int = None,
                             from_date: str = None, to_date: str = None,
                             limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取特定NFT的转账记录
    
    Args:
        token_address: NFT合约地址
        token_id: NFT的token ID
        chain: 区块链网络
        format: 格式(decimal或hex)
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        特定NFT的转账记录列表
    """
    params = {
        "address": token_address,
        "token_id": token_id,
        "chain": chain,
        "format": format,
        "limit": limit,
        "cursor": cursor
    }
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.nft.get_nft_token_id_transfers(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_contract_metadata(token_address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取NFT合约元数据
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
    
    Returns:
        NFT合约元数据
    """
    params = {
        "address": token_address,
        "chain": chain
    }
    
    result = evm_api.nft.get_nft_contract_metadata(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def sync_nft_contract(token_address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """同步NFT合约
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
    
    Returns:
        同步结果
    """
    params = {
        "address": token_address,
        "chain": chain
    }
    
    result = evm_api.nft.sync_nft_contract(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def resync_nft_metadata(token_address: str, token_id: str, chain: str = DEFAULT_CHAIN,
                      mode: str = "sync") -> Dict[str, Any]:
    """重新同步NFT元数据
    
    Args:
        token_address: NFT合约地址
        token_id: NFT的token ID
        chain: 区块链网络
        mode: 同步模式 (sync或async)
    
    Returns:
        同步结果
    """
    params = {
        "address": token_address,
        "token_id": token_id,
        "chain": chain,
        "mode": mode
    }
    
    result = evm_api.nft.resync_metadata(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_contract_traits(token_address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取NFT合约特征
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
    
    Returns:
        NFT合约特征列表
    """
    params = {
        "address": token_address,
        "chain": chain
    }
    
    result = evm_api.nft.get_nft_contract_traits(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_trades(chain: str = DEFAULT_CHAIN,
                 marketplace: str = None,
                 from_block: int = None, to_block: int = None,
                 from_date: str = None, to_date: str = None,
                 limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取NFT交易
    
    Args:
        chain: 区块链网络
        marketplace: 市场名称
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        NFT交易列表
    """
    params = {
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if marketplace:
        params["marketplace"] = marketplace
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.nft.get_nft_trades(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_contract_trades(token_address: str, chain: str = DEFAULT_CHAIN,
                          marketplace: str = None,
                          from_block: int = None, to_block: int = None,
                          from_date: str = None, to_date: str = None,
                          limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取NFT合约交易
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
        marketplace: 市场名称
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        NFT合约交易列表
    """
    params = {
        "address": token_address,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if marketplace:
        params["marketplace"] = marketplace
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.nft.get_nft_contract_trades(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_token_id_trades(token_address: str, token_id: str, chain: str = DEFAULT_CHAIN,
                          marketplace: str = None,
                          from_block: int = None, to_block: int = None,
                          from_date: str = None, to_date: str = None,
                          limit: int = DEFAULT_LIMIT, cursor: str = "") -> Dict[str, Any]:
    """获取特定NFT的交易
    
    Args:
        token_address: NFT合约地址
        token_id: NFT的token ID
        chain: 区块链网络
        marketplace: 市场名称
        from_block: 开始区块
        to_block: 结束区块
        from_date: 开始日期 (ISO-8601格式)
        to_date: 结束日期 (ISO-8601格式)
        limit: 每页返回数量
        cursor: 用于分页的游标
    
    Returns:
        特定NFT的交易列表
    """
    params = {
        "address": token_address,
        "token_id": token_id,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if marketplace:
        params["marketplace"] = marketplace
    
    if from_block:
        params["from_block"] = from_block
    
    if to_block:
        params["to_block"] = to_block
    
    if from_date:
        params["from_date"] = from_date
    
    if to_date:
        params["to_date"] = to_date
    
    result = evm_api.nft.get_nft_token_id_trades(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 价格API工具
@mcp.tool()
def get_nft_floor_price(token_address: str, chain: str = DEFAULT_CHAIN,
                      marketplace: str = None) -> Dict[str, Any]:
    """获取NFT地板价
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
        marketplace: 市场名称
    
    Returns:
        NFT地板价信息
    """
    params = {
        "address": token_address,
        "chain": chain
    }
    
    if marketplace:
        params["marketplace"] = marketplace
    
    result = evm_api.nft.get_nft_contract_floor_price(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_token_floor_price(token_address: str, token_id: str,
                            chain: str = DEFAULT_CHAIN,
                            marketplace: str = None) -> Dict[str, Any]:
    """获取特定NFT的地板价
    
    Args:
        token_address: NFT合约地址
        token_id: NFT的token ID
        chain: 区块链网络
        marketplace: 市场名称
    
    Returns:
        特定NFT的地板价信息
    """
    params = {
        "address": token_address,
        "token_id": token_id,
        "chain": chain
    }
    
    if marketplace:
        params["marketplace"] = marketplace
    
    result = evm_api.nft.get_nft_token_floor_price(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_nft_historical_floor_price(token_address: str, chain: str = DEFAULT_CHAIN,
                                 marketplace: str = None,
                                 days: int = 30) -> Dict[str, Any]:
    """获取NFT历史地板价
    
    Args:
        token_address: NFT合约地址
        chain: 区块链网络
        marketplace: 市场名称
        days: 天数
    
    Returns:
        NFT历史地板价信息
    """
    params = {
        "address": token_address,
        "chain": chain,
        "days": days
    }
    
    if marketplace:
        params["marketplace"] = marketplace
    
    result = evm_api.nft.get_nft_historical_floor_price(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 区块链API工具
@mcp.tool()
def get_block(block_number_or_hash: str, chain: str = DEFAULT_CHAIN,
            include_transactions: bool = False) -> Dict[str, Any]:
    """获取区块信息
    
    Args:
        block_number_or_hash: 区块号或哈希
        chain: 区块链网络
        include_transactions: 是否包含交易
    
    Returns:
        区块信息
    """
    params = {
        "block_number_or_hash": block_number_or_hash,
        "chain": chain,
        "include": include_transactions
    }
    
    result = evm_api.block.get_block(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_date_to_block(date: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """通过日期获取区块
    
    Args:
        date: 日期 (ISO-8601格式)
        chain: 区块链网络
    
    Returns:
        区块信息
    """
    params = {
        "date": date,
        "chain": chain
    }
    
    result = evm_api.block.get_date_to_block(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_transaction(transaction_hash: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取交易信息
    
    Args:
        transaction_hash: 交易哈希
        chain: 区块链网络
    
    Returns:
        交易信息
    """
    params = {
        "transaction_hash": transaction_hash,
        "chain": chain
    }
    
    result = evm_api.transaction.get_transaction(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_decoded_transaction(transaction_hash: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取已解码的交易信息
    
    Args:
        transaction_hash: 交易哈希
        chain: 区块链网络
    
    Returns:
        已解码的交易信息
    """
    params = {
        "transaction_hash": transaction_hash,
        "chain": chain
    }
    
    result = evm_api.transaction.get_decoded_transaction(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_internal_transactions(transaction_hash: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取内部交易
    
    Args:
        transaction_hash: 交易哈希
        chain: 区块链网络
    
    Returns:
        内部交易列表
    """
    params = {
        "transaction_hash": transaction_hash,
        "chain": chain
    }
    
    result = evm_api.transaction.get_internal_transactions(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_latest_block_number(chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取最新区块号
    
    Args:
        chain: 区块链网络
    
    Returns:
        最新区块号信息
    """
    params = {
        "chain": chain
    }
    
    result = evm_api.block.get_latest_block_number(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# DeFi API工具
@mcp.tool()
def get_defi_summary(address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取钱包的DeFi协议摘要
    
    Args:
        address: 钱包地址
        chain: 区块链网络
    
    Returns:
        DeFi协议摘要
    """
    params = {
        "address": address,
        "chain": chain
    }
    
    result = evm_api.defi.get_defi_summary(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_defi_positions(address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取钱包的DeFi持仓
    
    Args:
        address: 钱包地址
        chain: 区块链网络
    
    Returns:
        DeFi持仓信息
    """
    params = {
        "address": address,
        "chain": chain
    }
    
    result = evm_api.defi.get_defi_positions(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_defi_protocol_positions(address: str, protocol: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取钱包在特定协议的DeFi持仓
    
    Args:
        address: 钱包地址
        protocol: 协议名称
        chain: 区块链网络
    
    Returns:
        特定协议的DeFi持仓信息
    """
    params = {
        "address": address,
        "protocol": protocol,
        "chain": chain
    }
    
    result = evm_api.defi.get_defi_protocol_positions(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 解析器API工具
@mcp.tool()
def resolve_domain(domain: str, currency: str = "eth") -> Dict[str, Any]:
    """解析域名为地址
    
    Args:
        domain: 域名
        currency: 货币类型
    
    Returns:
        域名解析结果
    """
    params = {
        "domain": domain,
        "currency": currency
    }
    
    result = evm_api.resolve.resolve_domain(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def resolve_address(address: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """解析地址为域名
    
    Args:
        address: 地址
        chain: 区块链网络
    
    Returns:
        地址解析结果
    """
    params = {
        "address": address,
        "chain": chain
    }
    
    result = evm_api.resolve.resolve_address(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def resolve_ens_domain(domain: str) -> Dict[str, Any]:
    """解析ENS域名
    
    Args:
        domain: ENS域名
    
    Returns:
        ENS域名解析结果
    """
    params = {
        "domain": domain
    }
    
    result = evm_api.resolve.resolve_ens_domain(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 实体API工具
@mcp.tool()
def get_entities(chain: str = DEFAULT_CHAIN, limit: int = DEFAULT_LIMIT, 
               cursor: str = "", category: str = None) -> Dict[str, Any]:
    """获取实体列表
    
    Args:
        chain: 区块链网络
        limit: 每页返回数量
        cursor: 用于分页的游标
        category: 实体类别
    
    Returns:
        实体列表
    """
    params = {
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if category:
        params["category"] = category
    
    result = evm_api.entity.get_entities(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_entity_by_id(entity_id: str, chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """通过ID获取实体
    
    Args:
        entity_id: 实体ID
        chain: 区块链网络
    
    Returns:
        实体信息
    """
    params = {
        "entityId": entity_id,
        "chain": chain
    }
    
    result = evm_api.entity.get_entity_by_id(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def get_entity_categories(chain: str = DEFAULT_CHAIN) -> Dict[str, Any]:
    """获取实体类别
    
    Args:
        chain: 区块链网络
    
    Returns:
        实体类别列表
    """
    params = {
        "chain": chain
    }
    
    result = evm_api.entity.get_entity_categories(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

@mcp.tool()
def search_entities(query: str, chain: str = DEFAULT_CHAIN, 
                  limit: int = DEFAULT_LIMIT, cursor: str = "",
                  category: str = None) -> Dict[str, Any]:
    """搜索实体
    
    Args:
        query: 搜索关键词
        chain: 区块链网络
        limit: 每页返回数量
        cursor: 用于分页的游标
        category: 实体类别
    
    Returns:
        搜索结果
    """
    params = {
        "query": query,
        "chain": chain,
        "limit": limit,
        "cursor": cursor
    }
    
    if category:
        params["category"] = category
    
    result = evm_api.entity.search_entities(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

# 工具类API
@mcp.tool()
def get_web3_api_version() -> Dict[str, Any]:
    """获取Web3 API版本
    
    Returns:
        API版本信息
    """
    result = evm_api.utils.web3_api_version(
        api_key=MORALIS_API_KEY
    )
    
    return result

@mcp.tool()
def get_endpoint_weights() -> Dict[str, Any]:
    """获取端点权重
    
    Returns:
        端点权重信息
    """
    result = evm_api.utils.get_endpoint_weights(
        api_key=MORALIS_API_KEY
    )
    
    return result

@mcp.tool()
def review_contracts(abi: List[Dict[str, Any]]) -> Dict[str, Any]:
    """审查合约
    
    Args:
        abi: 合约ABI
    
    Returns:
        合约审查结果
    """
    params = {
        "abi": abi
    }
    
    result = evm_api.utils.review_contracts(
        api_key=MORALIS_API_KEY,
        params=params
    )
    
    return result

def main():
    """
    MCP服务器的主入口点
    """
    # 检查必要的环境变量是否配置
    if not MORALIS_API_KEY:
        print("错误: 未配置MORALIS_API_KEY环境变量。请在.env文件中设置MORALIS_API_KEY。")
        exit(1)
    
    print(f"环境变量检查通过: MORALIS_API_KEY已配置")
    print(f"默认链设置为: {DEFAULT_CHAIN}")
    print(f"默认限制设置为: {DEFAULT_LIMIT}")
    
    # 运行MCP服务器
    mcp.run()

if __name__ == "__main__":
    main() 