import logging
from datetime import datetime
from flask import render_template, jsonify, request
from app import app, db
from models import SpotTicker, FetchLog, MarketList, OrderbookSnapshot
from adapters import LBankAdapter, HashKeyAdapter, BiconomyAdapter, MEXCAdapter, BitrueAdapter, AscendEXAdapter, BitMartAdapter, DexTradeAdapter, PoloniexAdapter, GateIOAdapter, NizaAdapter, XTAdapter, CoinstoreAdapter, VindaxAdapter, FameEXAdapter, BigOneAdapter, P2PB2BAdapter, DigiFinexAdapter, AzbitAdapter, LatokenAdapter, KrakenAdapter, BingXAdapter, BTSEAdapter, WhiteBitAdapter, HTXAdapter, BinanceAlphaAdapter, UZXAdapter

logger = logging.getLogger(__name__)


def get_adapter(exchange):
    """Return an adapter instance for the given exchange name, or None."""
    adapter_map = {
        'LBANK': LBankAdapter, 'HASHKEY': HashKeyAdapter, 'BICONOMY': BiconomyAdapter,
        'MEXC': MEXCAdapter, 'BITRUE': BitrueAdapter, 'ASCENDEX': AscendEXAdapter,
        'BITMART': BitMartAdapter, 'DEXTRADE': DexTradeAdapter, 'POLONIEX': PoloniexAdapter,
        'GATEIO': GateIOAdapter, 'NIZA': NizaAdapter, 'XT': XTAdapter,
        'COINSTORE': CoinstoreAdapter, 'VINDAX': VindaxAdapter, 'FAMEEX': FameEXAdapter,
        'BIGONE': BigOneAdapter, 'P2PB2B': P2PB2BAdapter, 'DIGIFINEX': DigiFinexAdapter,
        'AZBIT': AzbitAdapter, 'LATOKEN': LatokenAdapter, 'KRAKEN': KrakenAdapter,
        'BINGX': BingXAdapter, 'BTSE': BTSEAdapter, 'WHITEBIT': WhiteBitAdapter,
        'HTX': HTXAdapter, 'BINANCEALPHA': BinanceAlphaAdapter, 'UZX': UZXAdapter,
    }
    cls = adapter_map.get(exchange.upper())
    return cls() if cls else None


def save_tickers(tickers, exchange_name):
    SpotTicker.query.filter_by(exchange=exchange_name).delete()
    
    for ticker in tickers:
        spot_ticker = SpotTicker(
            exchange=ticker.exchange,
            symbol=ticker.symbol,
            base_currency=ticker.base_currency,
            quote_currency=ticker.quote_currency,
            price=ticker.price,
            volume_24h=ticker.volume_24h,
            high_24h=ticker.high_24h,
            low_24h=ticker.low_24h,
            change_24h=ticker.change_24h,
            turnover_24h=ticker.turnover_24h,
            fetched_at=datetime.utcnow()
        )
        db.session.add(spot_ticker)
    
    db.session.commit()


def log_fetch(exchange_name, status, pairs_count=0, error_message=None):
    log = FetchLog(
        exchange=exchange_name,
        status=status,
        pairs_count=pairs_count,
        error_message=error_message,
        fetched_at=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/fetch/lbank', methods=['POST'])
def fetch_lbank():
    try:
        adapter = LBankAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from LBANK'
        })
    except Exception as e:
        log_fetch('LBANK', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'LBANK',
            'message': str(e)
        }), 500


@app.route('/api/fetch/hashkey', methods=['POST'])
def fetch_hashkey():
    try:
        adapter = HashKeyAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from HashKey'
        })
    except Exception as e:
        log_fetch('HASHKEY', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'HASHKEY',
            'message': str(e)
        }), 500


@app.route('/api/fetch/biconomy', methods=['POST'])
def fetch_biconomy():
    try:
        adapter = BiconomyAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Biconomy'
        })
    except Exception as e:
        log_fetch('BICONOMY', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BICONOMY',
            'message': str(e)
        }), 500


@app.route('/api/fetch/mexc', methods=['POST'])
def fetch_mexc():
    try:
        adapter = MEXCAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from MEXC'
        })
    except Exception as e:
        log_fetch('MEXC', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'MEXC',
            'message': str(e)
        }), 500


@app.route('/api/fetch/bitrue', methods=['POST'])
def fetch_bitrue():
    try:
        adapter = BitrueAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Bitrue'
        })
    except Exception as e:
        log_fetch('BITRUE', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BITRUE',
            'message': str(e)
        }), 500


@app.route('/api/fetch/ascendex', methods=['POST'])
def fetch_ascendex():
    try:
        adapter = AscendEXAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from AscendEX'
        })
    except Exception as e:
        log_fetch('ASCENDEX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'ASCENDEX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/bitmart', methods=['POST'])
def fetch_bitmart():
    try:
        adapter = BitMartAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from BitMart'
        })
    except Exception as e:
        log_fetch('BITMART', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BITMART',
            'message': str(e)
        }), 500


@app.route('/api/fetch/dextrade', methods=['POST'])
def fetch_dextrade():
    try:
        adapter = DexTradeAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Dex-Trade'
        })
    except Exception as e:
        log_fetch('DEXTRADE', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'DEXTRADE',
            'message': str(e)
        }), 500


@app.route('/api/fetch/poloniex', methods=['POST'])
def fetch_poloniex():
    try:
        adapter = PoloniexAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Poloniex'
        })
    except Exception as e:
        log_fetch('POLONIEX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'POLONIEX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/gateio', methods=['POST'])
def fetch_gateio():
    try:
        adapter = GateIOAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Gate.io'
        })
    except Exception as e:
        log_fetch('GATEIO', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'GATEIO',
            'message': str(e)
        }), 500


@app.route('/api/fetch/niza', methods=['POST'])
def fetch_niza():
    try:
        adapter = NizaAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Niza'
        })
    except Exception as e:
        log_fetch('NIZA', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'NIZA',
            'message': str(e)
        }), 500


@app.route('/api/fetch/xt', methods=['POST'])
def fetch_xt():
    try:
        adapter = XTAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from XT.com'
        })
    except Exception as e:
        log_fetch('XT', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'XT',
            'message': str(e)
        }), 500


@app.route('/api/fetch/coinstore', methods=['POST'])
def fetch_coinstore():
    try:
        adapter = CoinstoreAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Coinstore'
        })
    except Exception as e:
        log_fetch('COINSTORE', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'COINSTORE',
            'message': str(e)
        }), 500


@app.route('/api/fetch/vindax', methods=['POST'])
def fetch_vindax():
    try:
        adapter = VindaxAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Vindax'
        })
    except Exception as e:
        log_fetch('VINDAX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'VINDAX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/fameex', methods=['POST'])
def fetch_fameex():
    try:
        adapter = FameEXAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from FameEX'
        })
    except Exception as e:
        log_fetch('FAMEEX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'FAMEEX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/bigone', methods=['POST'])
def fetch_bigone():
    try:
        adapter = BigOneAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from BigOne'
        })
    except Exception as e:
        log_fetch('BIGONE', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BIGONE',
            'message': str(e)
        }), 500


@app.route('/api/fetch/p2pb2b', methods=['POST'])
def fetch_p2pb2b():
    try:
        adapter = P2PB2BAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from P2PB2B'
        })
    except Exception as e:
        log_fetch('P2PB2B', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'P2PB2B',
            'message': str(e)
        }), 500


@app.route('/api/fetch/digifinex', methods=['POST'])
def fetch_digifinex():
    try:
        adapter = DigiFinexAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from DigiFinex'
        })
    except Exception as e:
        log_fetch('DIGIFINEX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'DIGIFINEX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/azbit', methods=['POST'])
def fetch_azbit():
    try:
        adapter = AzbitAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Azbit'
        })
    except Exception as e:
        log_fetch('AZBIT', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'AZBIT',
            'message': str(e)
        }), 500


@app.route('/api/fetch/latoken', methods=['POST'])
def fetch_latoken():
    try:
        adapter = LatokenAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from LATOKEN'
        })
    except Exception as e:
        log_fetch('LATOKEN', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'LATOKEN',
            'message': str(e)
        }), 500



@app.route('/api/fetch/bingx', methods=['POST'])
def fetch_bingx():
    try:
        adapter = BingXAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))
        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from BingX'
        })
    except Exception as e:
        log_fetch('BINGX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BINGX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/kraken', methods=['POST'])
def fetch_kraken():
    try:
        adapter = KrakenAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))

        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from Kraken'
        })
    except Exception as e:
        log_fetch('KRAKEN', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'KRAKEN',
            'message': str(e)
        }), 500


@app.route('/api/tickers')
def get_tickers():
    draw = request.args.get('draw', 1, type=int)
    start = request.args.get('start', 0, type=int)
    length = request.args.get('length', 50, type=int)
    search_value = request.args.get('search[value]', '', type=str)
    exchange_filter = request.args.get('exchange', '', type=str)
    multi_exchange = request.args.get('multi_exchange', 'false', type=str) == 'true'
    list_filter = request.args.get('list_filter', '', type=str)
    exclude_leveraged = request.args.get('exclude_leveraged', 'false', type=str) == 'true'
    order_column = request.args.get('order[0][column]', '1', type=str)
    order_dir = request.args.get('order[0][dir]', 'asc', type=str)
    
    column_map = {
        '0': SpotTicker.exchange,
        '1': SpotTicker.symbol,
        '2': SpotTicker.change_24h,
        '3': SpotTicker.turnover_24h,
        '4': None,
        '5': SpotTicker.price,
        '6': None,
        '7': None
    }
    
    query = SpotTicker.query
    
    if exchange_filter:
        query = query.filter(SpotTicker.exchange == exchange_filter)

    if exclude_leveraged:
        import re as _re
        _leveraged = _re.compile(r'\d+[LSls](USDT)?$')
        leveraged_symbols = [
            t.symbol for t in SpotTicker.query.with_entities(SpotTicker.symbol).distinct()
            if _leveraged.search(t.symbol.split('/')[0])
        ]
        if leveraged_symbols:
            query = query.filter(SpotTicker.symbol.notin_(leveraged_symbols))

    if search_value:
        query = query.filter(
            db.or_(
                SpotTicker.symbol.ilike(f'%{search_value}%'),
                SpotTicker.base_currency.ilike(f'%{search_value}%')
            )
        )
    
    if multi_exchange:
        from sqlalchemy import func
        symbol_counts = db.session.query(
            SpotTicker.symbol,
            func.count(SpotTicker.exchange).label('exchange_count')
        ).group_by(SpotTicker.symbol).having(func.count(SpotTicker.exchange) > 1).subquery()
        
        query = query.join(symbol_counts, SpotTicker.symbol == symbol_counts.c.symbol)
    
    blacklist_entries = MarketList.query.filter_by(list_type='blacklist').all()
    whitelist_entries = MarketList.query.filter_by(list_type='whitelist').all()
    walletlock_entries = MarketList.query.filter_by(list_type='wallet_lock').all()
    blacklist_set = {(e.exchange, e.symbol) for e in blacklist_entries}
    whitelist_set = {(e.exchange, e.symbol) for e in whitelist_entries}
    walletlock_set = {(e.exchange, e.symbol) for e in walletlock_entries}
    
    from sqlalchemy import or_, and_, not_, tuple_
    
    if list_filter == 'hide_blacklist' and blacklist_set:
        blacklist_conditions = [and_(SpotTicker.exchange == ex, SpotTicker.symbol == sym) for ex, sym in blacklist_set]
        query = query.filter(not_(or_(*blacklist_conditions)))
    elif list_filter == 'only_whitelist':
        if whitelist_set:
            conditions = [and_(SpotTicker.exchange == ex, SpotTicker.symbol == sym) for ex, sym in whitelist_set]
            query = query.filter(or_(*conditions))
        else:
            query = query.filter(db.literal(False))
    elif list_filter == 'only_blacklist':
        if blacklist_set:
            conditions = [and_(SpotTicker.exchange == ex, SpotTicker.symbol == sym) for ex, sym in blacklist_set]
            query = query.filter(or_(*conditions))
        else:
            query = query.filter(db.literal(False))
    
    total_records = SpotTicker.query.count()
    filtered_records = query.count()
    
    from sqlalchemy import func
    if exchange_filter:
        base_query = SpotTicker.query.filter(SpotTicker.exchange == exchange_filter)
        if search_value:
            base_query = base_query.filter(
                db.or_(
                    SpotTicker.symbol.ilike(f'%{search_value}%'),
                    SpotTicker.base_currency.ilike(f'%{search_value}%')
                )
            )
        filtered_symbols = [t.symbol for t in base_query.all()]
        multi_symbol_counts = db.session.query(
            SpotTicker.symbol
        ).filter(SpotTicker.symbol.in_(filtered_symbols)).group_by(SpotTicker.symbol).having(func.count(SpotTicker.exchange) > 1).all()
        comparable_pairs = len(multi_symbol_counts)
    else:
        multi_symbol_counts = db.session.query(
            SpotTicker.symbol
        ).group_by(SpotTicker.symbol).having(func.count(SpotTicker.exchange) > 1).all()
        comparable_pairs = len(multi_symbol_counts)
    
    order_col = column_map.get(order_column, SpotTicker.symbol)
    if order_col is not None:
        if order_dir == 'desc':
            query = query.order_by(order_col.desc())
        else:
            query = query.order_by(order_col.asc())
    else:
        query = query.order_by(SpotTicker.symbol.asc())
    
    tickers = query.offset(start).limit(length).all()
    
    all_tickers = SpotTicker.query.all()
    symbol_map = {}
    for t in all_tickers:
        if t.symbol not in symbol_map:
            symbol_map[t.symbol] = {}
        ticker_data = t.to_dict()
        ticker_data['is_blacklisted'] = (t.exchange, t.symbol) in blacklist_set
        symbol_map[t.symbol][t.exchange] = ticker_data
    
    data = []
    for t in tickers:
        ticker_dict = t.to_dict()
        peers = []
        if t.symbol in symbol_map:
            for ex, peer_data in symbol_map[t.symbol].items():
                if ex != t.exchange:
                    peers.append(peer_data)
        ticker_dict['peers'] = peers
        ticker_dict['exchange_count'] = len(symbol_map.get(t.symbol, {}))
        ticker_dict['is_blacklisted'] = (t.exchange, t.symbol) in blacklist_set
        ticker_dict['is_whitelisted'] = (t.exchange, t.symbol) in whitelist_set
        ticker_dict['is_wallet_locked'] = (t.exchange, t.symbol) in walletlock_set
        data.append(ticker_dict)
    
    return jsonify({
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': filtered_records,
        'comparablePairs': comparable_pairs,
        'data': data
    })


@app.route('/api/logs')
def get_logs():
    logs = FetchLog.query.order_by(FetchLog.fetched_at.desc()).limit(20).all()
    return jsonify({
        'status': 'success',
        'data': [log.to_dict() for log in logs]
    })


@app.route('/api/status')
def get_status():
    lbank_log = FetchLog.query.filter_by(exchange='LBANK').order_by(FetchLog.fetched_at.desc()).first()
    hashkey_log = FetchLog.query.filter_by(exchange='HASHKEY').order_by(FetchLog.fetched_at.desc()).first()
    biconomy_log = FetchLog.query.filter_by(exchange='BICONOMY').order_by(FetchLog.fetched_at.desc()).first()
    mexc_log = FetchLog.query.filter_by(exchange='MEXC').order_by(FetchLog.fetched_at.desc()).first()
    bitrue_log = FetchLog.query.filter_by(exchange='BITRUE').order_by(FetchLog.fetched_at.desc()).first()
    ascendex_log = FetchLog.query.filter_by(exchange='ASCENDEX').order_by(FetchLog.fetched_at.desc()).first()
    bitmart_log = FetchLog.query.filter_by(exchange='BITMART').order_by(FetchLog.fetched_at.desc()).first()
    dextrade_log = FetchLog.query.filter_by(exchange='DEXTRADE').order_by(FetchLog.fetched_at.desc()).first()
    poloniex_log = FetchLog.query.filter_by(exchange='POLONIEX').order_by(FetchLog.fetched_at.desc()).first()
    gateio_log = FetchLog.query.filter_by(exchange='GATEIO').order_by(FetchLog.fetched_at.desc()).first()
    niza_log = FetchLog.query.filter_by(exchange='NIZA').order_by(FetchLog.fetched_at.desc()).first()
    xt_log = FetchLog.query.filter_by(exchange='XT').order_by(FetchLog.fetched_at.desc()).first()
    coinstore_log = FetchLog.query.filter_by(exchange='COINSTORE').order_by(FetchLog.fetched_at.desc()).first()
    vindax_log = FetchLog.query.filter_by(exchange='VINDAX').order_by(FetchLog.fetched_at.desc()).first()
    fameex_log = FetchLog.query.filter_by(exchange='FAMEEX').order_by(FetchLog.fetched_at.desc()).first()
    bigone_log = FetchLog.query.filter_by(exchange='BIGONE').order_by(FetchLog.fetched_at.desc()).first()
    p2pb2b_log = FetchLog.query.filter_by(exchange='P2PB2B').order_by(FetchLog.fetched_at.desc()).first()
    digifinex_log = FetchLog.query.filter_by(exchange='DIGIFINEX').order_by(FetchLog.fetched_at.desc()).first()
    azbit_log = FetchLog.query.filter_by(exchange='AZBIT').order_by(FetchLog.fetched_at.desc()).first()
    latoken_log = FetchLog.query.filter_by(exchange='LATOKEN').order_by(FetchLog.fetched_at.desc()).first()
    kraken_log = FetchLog.query.filter_by(exchange='KRAKEN').order_by(FetchLog.fetched_at.desc()).first()
    bingx_log = FetchLog.query.filter_by(exchange='BINGX').order_by(FetchLog.fetched_at.desc()).first()
    btse_log = FetchLog.query.filter_by(exchange='BTSE').order_by(FetchLog.fetched_at.desc()).first()
    whitebit_log = FetchLog.query.filter_by(exchange='WHITEBIT').order_by(FetchLog.fetched_at.desc()).first()
    htx_log = FetchLog.query.filter_by(exchange='HTX').order_by(FetchLog.fetched_at.desc()).first()
    binancealpha_log = FetchLog.query.filter_by(exchange='BINANCEALPHA').order_by(FetchLog.fetched_at.desc()).first()
    uzx_log = FetchLog.query.filter_by(exchange='UZX').order_by(FetchLog.fetched_at.desc()).first()
    
    lbank_count = SpotTicker.query.filter_by(exchange='LBANK').count()
    hashkey_count = SpotTicker.query.filter_by(exchange='HASHKEY').count()
    biconomy_count = SpotTicker.query.filter_by(exchange='BICONOMY').count()
    mexc_count = SpotTicker.query.filter_by(exchange='MEXC').count()
    bitrue_count = SpotTicker.query.filter_by(exchange='BITRUE').count()
    ascendex_count = SpotTicker.query.filter_by(exchange='ASCENDEX').count()
    bitmart_count = SpotTicker.query.filter_by(exchange='BITMART').count()
    dextrade_count = SpotTicker.query.filter_by(exchange='DEXTRADE').count()
    poloniex_count = SpotTicker.query.filter_by(exchange='POLONIEX').count()
    gateio_count = SpotTicker.query.filter_by(exchange='GATEIO').count()
    niza_count = SpotTicker.query.filter_by(exchange='NIZA').count()
    xt_count = SpotTicker.query.filter_by(exchange='XT').count()
    coinstore_count = SpotTicker.query.filter_by(exchange='COINSTORE').count()
    vindax_count = SpotTicker.query.filter_by(exchange='VINDAX').count()
    fameex_count = SpotTicker.query.filter_by(exchange='FAMEEX').count()
    bigone_count = SpotTicker.query.filter_by(exchange='BIGONE').count()
    p2pb2b_count = SpotTicker.query.filter_by(exchange='P2PB2B').count()
    digifinex_count = SpotTicker.query.filter_by(exchange='DIGIFINEX').count()
    azbit_count = SpotTicker.query.filter_by(exchange='AZBIT').count()
    latoken_count = SpotTicker.query.filter_by(exchange='LATOKEN').count()
    kraken_count = SpotTicker.query.filter_by(exchange='KRAKEN').count()
    bingx_count = SpotTicker.query.filter_by(exchange='BINGX').count()
    btse_count = SpotTicker.query.filter_by(exchange='BTSE').count()
    whitebit_count = SpotTicker.query.filter_by(exchange='WHITEBIT').count()
    htx_count = SpotTicker.query.filter_by(exchange='HTX').count()
    binancealpha_count = SpotTicker.query.filter_by(exchange='BINANCEALPHA').count()
    uzx_count = SpotTicker.query.filter_by(exchange='UZX').count()
    
    exchanges = ['LBANK', 'HASHKEY', 'BICONOMY', 'MEXC', 'BITRUE', 'ASCENDEX', 
                 'BITMART', 'DEXTRADE', 'POLONIEX', 'GATEIO', 'NIZA', 'XT', 
                 'COINSTORE', 'VINDAX', 'FAMEEX', 'BIGONE', 'P2PB2B', 'DIGIFINEX', 'AZBIT', 'LATOKEN', 'KRAKEN', 'BINGX', 'BTSE', 'WHITEBIT', 'HTX', 'BINANCEALPHA', 'UZX']
    
    from sqlalchemy import func
    blacklist_counts = dict(db.session.query(
        MarketList.exchange, func.count(MarketList.id)
    ).filter_by(list_type='blacklist').group_by(MarketList.exchange).all())
    
    whitelist_counts = dict(db.session.query(
        MarketList.exchange, func.count(MarketList.id)
    ).filter_by(list_type='whitelist').group_by(MarketList.exchange).all())
    
    walletlock_counts = dict(db.session.query(
        MarketList.exchange, func.count(MarketList.id)
    ).filter_by(list_type='wallet_lock').group_by(MarketList.exchange).all())
    
    return jsonify({
        'lbank': {
            'last_fetch': lbank_log.fetched_at.isoformat() if lbank_log else None,
            'status': lbank_log.status if lbank_log else 'never',
            'pairs_count': lbank_count,
            'blacklist_count': blacklist_counts.get('LBANK', 0),
            'whitelist_count': whitelist_counts.get('LBANK', 0),
            'walletlock_count': walletlock_counts.get('LBANK', 0)
        },
        'hashkey': {
            'last_fetch': hashkey_log.fetched_at.isoformat() if hashkey_log else None,
            'status': hashkey_log.status if hashkey_log else 'never',
            'pairs_count': hashkey_count,
            'blacklist_count': blacklist_counts.get('HASHKEY', 0),
            'whitelist_count': whitelist_counts.get('HASHKEY', 0),
            'walletlock_count': walletlock_counts.get('HASHKEY', 0)
        },
        'biconomy': {
            'last_fetch': biconomy_log.fetched_at.isoformat() if biconomy_log else None,
            'status': biconomy_log.status if biconomy_log else 'never',
            'pairs_count': biconomy_count,
            'blacklist_count': blacklist_counts.get('BICONOMY', 0),
            'whitelist_count': whitelist_counts.get('BICONOMY', 0),
            'walletlock_count': walletlock_counts.get('BICONOMY', 0)
        },
        'mexc': {
            'last_fetch': mexc_log.fetched_at.isoformat() if mexc_log else None,
            'status': mexc_log.status if mexc_log else 'never',
            'pairs_count': mexc_count,
            'blacklist_count': blacklist_counts.get('MEXC', 0),
            'whitelist_count': whitelist_counts.get('MEXC', 0),
            'walletlock_count': walletlock_counts.get('MEXC', 0)
        },
        'bitrue': {
            'last_fetch': bitrue_log.fetched_at.isoformat() if bitrue_log else None,
            'status': bitrue_log.status if bitrue_log else 'never',
            'pairs_count': bitrue_count,
            'blacklist_count': blacklist_counts.get('BITRUE', 0),
            'whitelist_count': whitelist_counts.get('BITRUE', 0),
            'walletlock_count': walletlock_counts.get('BITRUE', 0)
        },
        'ascendex': {
            'last_fetch': ascendex_log.fetched_at.isoformat() if ascendex_log else None,
            'status': ascendex_log.status if ascendex_log else 'never',
            'pairs_count': ascendex_count,
            'blacklist_count': blacklist_counts.get('ASCENDEX', 0),
            'whitelist_count': whitelist_counts.get('ASCENDEX', 0),
            'walletlock_count': walletlock_counts.get('ASCENDEX', 0)
        },
        'bitmart': {
            'last_fetch': bitmart_log.fetched_at.isoformat() if bitmart_log else None,
            'status': bitmart_log.status if bitmart_log else 'never',
            'pairs_count': bitmart_count,
            'blacklist_count': blacklist_counts.get('BITMART', 0),
            'whitelist_count': whitelist_counts.get('BITMART', 0),
            'walletlock_count': walletlock_counts.get('BITMART', 0)
        },
        'dextrade': {
            'last_fetch': dextrade_log.fetched_at.isoformat() if dextrade_log else None,
            'status': dextrade_log.status if dextrade_log else 'never',
            'pairs_count': dextrade_count,
            'blacklist_count': blacklist_counts.get('DEXTRADE', 0),
            'whitelist_count': whitelist_counts.get('DEXTRADE', 0),
            'walletlock_count': walletlock_counts.get('DEXTRADE', 0)
        },
        'poloniex': {
            'last_fetch': poloniex_log.fetched_at.isoformat() if poloniex_log else None,
            'status': poloniex_log.status if poloniex_log else 'never',
            'pairs_count': poloniex_count,
            'blacklist_count': blacklist_counts.get('POLONIEX', 0),
            'whitelist_count': whitelist_counts.get('POLONIEX', 0),
            'walletlock_count': walletlock_counts.get('POLONIEX', 0)
        },
        'gateio': {
            'last_fetch': gateio_log.fetched_at.isoformat() if gateio_log else None,
            'status': gateio_log.status if gateio_log else 'never',
            'pairs_count': gateio_count,
            'blacklist_count': blacklist_counts.get('GATEIO', 0),
            'whitelist_count': whitelist_counts.get('GATEIO', 0),
            'walletlock_count': walletlock_counts.get('GATEIO', 0)
        },
        'niza': {
            'last_fetch': niza_log.fetched_at.isoformat() if niza_log else None,
            'status': niza_log.status if niza_log else 'never',
            'pairs_count': niza_count,
            'blacklist_count': blacklist_counts.get('NIZA', 0),
            'whitelist_count': whitelist_counts.get('NIZA', 0),
            'walletlock_count': walletlock_counts.get('NIZA', 0)
        },
        'xt': {
            'last_fetch': xt_log.fetched_at.isoformat() if xt_log else None,
            'status': xt_log.status if xt_log else 'never',
            'pairs_count': xt_count,
            'blacklist_count': blacklist_counts.get('XT', 0),
            'whitelist_count': whitelist_counts.get('XT', 0),
            'walletlock_count': walletlock_counts.get('XT', 0)
        },
        'coinstore': {
            'last_fetch': coinstore_log.fetched_at.isoformat() if coinstore_log else None,
            'status': coinstore_log.status if coinstore_log else 'never',
            'pairs_count': coinstore_count,
            'blacklist_count': blacklist_counts.get('COINSTORE', 0),
            'whitelist_count': whitelist_counts.get('COINSTORE', 0),
            'walletlock_count': walletlock_counts.get('COINSTORE', 0)
        },
        'vindax': {
            'last_fetch': vindax_log.fetched_at.isoformat() if vindax_log else None,
            'status': vindax_log.status if vindax_log else 'never',
            'pairs_count': vindax_count,
            'blacklist_count': blacklist_counts.get('VINDAX', 0),
            'whitelist_count': whitelist_counts.get('VINDAX', 0),
            'walletlock_count': walletlock_counts.get('VINDAX', 0)
        },
        'fameex': {
            'last_fetch': fameex_log.fetched_at.isoformat() if fameex_log else None,
            'status': fameex_log.status if fameex_log else 'never',
            'pairs_count': fameex_count,
            'blacklist_count': blacklist_counts.get('FAMEEX', 0),
            'whitelist_count': whitelist_counts.get('FAMEEX', 0),
            'walletlock_count': walletlock_counts.get('FAMEEX', 0)
        },
        'bigone': {
            'last_fetch': bigone_log.fetched_at.isoformat() if bigone_log else None,
            'status': bigone_log.status if bigone_log else 'never',
            'pairs_count': bigone_count,
            'blacklist_count': blacklist_counts.get('BIGONE', 0),
            'whitelist_count': whitelist_counts.get('BIGONE', 0),
            'walletlock_count': walletlock_counts.get('BIGONE', 0)
        },
        'p2pb2b': {
            'last_fetch': p2pb2b_log.fetched_at.isoformat() if p2pb2b_log else None,
            'status': p2pb2b_log.status if p2pb2b_log else 'never',
            'pairs_count': p2pb2b_count,
            'blacklist_count': blacklist_counts.get('P2PB2B', 0),
            'whitelist_count': whitelist_counts.get('P2PB2B', 0),
            'walletlock_count': walletlock_counts.get('P2PB2B', 0)
        },
        'digifinex': {
            'last_fetch': digifinex_log.fetched_at.isoformat() if digifinex_log else None,
            'status': digifinex_log.status if digifinex_log else 'never',
            'pairs_count': digifinex_count,
            'blacklist_count': blacklist_counts.get('DIGIFINEX', 0),
            'whitelist_count': whitelist_counts.get('DIGIFINEX', 0),
            'walletlock_count': walletlock_counts.get('DIGIFINEX', 0)
        },
        'azbit': {
            'last_fetch': azbit_log.fetched_at.isoformat() if azbit_log else None,
            'status': azbit_log.status if azbit_log else 'never',
            'pairs_count': azbit_count,
            'blacklist_count': blacklist_counts.get('AZBIT', 0),
            'whitelist_count': whitelist_counts.get('AZBIT', 0),
            'walletlock_count': walletlock_counts.get('AZBIT', 0)
        },
        'latoken': {
            'last_fetch': latoken_log.fetched_at.isoformat() if latoken_log else None,
            'status': latoken_log.status if latoken_log else 'never',
            'pairs_count': latoken_count,
            'blacklist_count': blacklist_counts.get('LATOKEN', 0),
            'whitelist_count': whitelist_counts.get('LATOKEN', 0),
            'walletlock_count': walletlock_counts.get('LATOKEN', 0)
        },
        'kraken': {
            'last_fetch': kraken_log.fetched_at.isoformat() if kraken_log else None,
            'status': kraken_log.status if kraken_log else 'never',
            'pairs_count': kraken_count,
            'blacklist_count': blacklist_counts.get('KRAKEN', 0),
            'whitelist_count': whitelist_counts.get('KRAKEN', 0),
            'walletlock_count': walletlock_counts.get('KRAKEN', 0)
        },
        'bingx': {
            'last_fetch': bingx_log.fetched_at.isoformat() if bingx_log else None,
            'status': bingx_log.status if bingx_log else 'never',
            'pairs_count': bingx_count,
            'blacklist_count': blacklist_counts.get('BINGX', 0),
            'whitelist_count': whitelist_counts.get('BINGX', 0),
            'walletlock_count': walletlock_counts.get('BINGX', 0)
        },
        'btse': {
            'last_fetch': btse_log.fetched_at.isoformat() if btse_log else None,
            'status': btse_log.status if btse_log else 'never',
            'pairs_count': btse_count,
            'blacklist_count': blacklist_counts.get('BTSE', 0),
            'whitelist_count': whitelist_counts.get('BTSE', 0),
            'walletlock_count': walletlock_counts.get('BTSE', 0)
        },
        'whitebit': {
            'last_fetch': whitebit_log.fetched_at.isoformat() if whitebit_log else None,
            'status': whitebit_log.status if whitebit_log else 'never',
            'pairs_count': whitebit_count,
            'blacklist_count': blacklist_counts.get('WHITEBIT', 0),
            'whitelist_count': whitelist_counts.get('WHITEBIT', 0),
            'walletlock_count': walletlock_counts.get('WHITEBIT', 0)
        },
        'htx': {
            'last_fetch': htx_log.fetched_at.isoformat() if htx_log else None,
            'status': htx_log.status if htx_log else 'never',
            'pairs_count': htx_count,
            'blacklist_count': blacklist_counts.get('HTX', 0),
            'whitelist_count': whitelist_counts.get('HTX', 0),
            'walletlock_count': walletlock_counts.get('HTX', 0)
        },
        'binancealpha': {
            'last_fetch': binancealpha_log.fetched_at.isoformat() if binancealpha_log else None,
            'status': binancealpha_log.status if binancealpha_log else 'never',
            'pairs_count': binancealpha_count,
            'blacklist_count': blacklist_counts.get('BINANCEALPHA', 0),
            'whitelist_count': whitelist_counts.get('BINANCEALPHA', 0),
            'walletlock_count': walletlock_counts.get('BINANCEALPHA', 0)
        },
        'uzx': {
            'last_fetch': uzx_log.fetched_at.isoformat() if uzx_log else None,
            'status': uzx_log.status if uzx_log else 'never',
            'pairs_count': uzx_count,
            'blacklist_count': blacklist_counts.get('UZX', 0),
            'whitelist_count': whitelist_counts.get('UZX', 0),
            'walletlock_count': walletlock_counts.get('UZX', 0)
        }
    })


@app.route('/api/depth/<exchange>/<path:symbol>')
def get_depth(exchange, symbol):
    """Get mini orderbook depth (top 5 bids/asks with total USDT)"""
    try:
        if exchange.upper() == 'LBANK':
            adapter = LBankAdapter()
        elif exchange.upper() == 'HASHKEY':
            adapter = HashKeyAdapter()
        elif exchange.upper() == 'BICONOMY':
            adapter = BiconomyAdapter()
        elif exchange.upper() == 'MEXC':
            adapter = MEXCAdapter()
        elif exchange.upper() == 'BITRUE':
            adapter = BitrueAdapter()
        elif exchange.upper() == 'ASCENDEX':
            adapter = AscendEXAdapter()
        elif exchange.upper() == 'BITMART':
            adapter = BitMartAdapter()
        elif exchange.upper() == 'DEXTRADE':
            adapter = DexTradeAdapter()
        elif exchange.upper() == 'POLONIEX':
            adapter = PoloniexAdapter()
        elif exchange.upper() == 'GATEIO':
            adapter = GateIOAdapter()
        elif exchange.upper() == 'NIZA':
            adapter = NizaAdapter()
        elif exchange.upper() == 'XT':
            adapter = XTAdapter()
        elif exchange.upper() == 'COINSTORE':
            adapter = CoinstoreAdapter()
        elif exchange.upper() == 'VINDAX':
            adapter = VindaxAdapter()
        elif exchange.upper() == 'FAMEEX':
            adapter = FameEXAdapter()
        elif exchange.upper() == 'BIGONE':
            adapter = BigOneAdapter()
        elif exchange.upper() == 'P2PB2B':
            adapter = P2PB2BAdapter()
        elif exchange.upper() == 'DIGIFINEX':
            adapter = DigiFinexAdapter()
        elif exchange.upper() == 'AZBIT':
            adapter = AzbitAdapter()
        elif exchange.upper() == 'LATOKEN':
            adapter = LatokenAdapter()
        elif exchange.upper() == 'KRAKEN':
            adapter = KrakenAdapter()
        elif exchange.upper() == 'BINGX':
            adapter = BingXAdapter()
        elif exchange.upper() == 'BTSE':
            adapter = BTSEAdapter()
        elif exchange.upper() == 'WHITEBIT':
            adapter = WhiteBitAdapter()
        elif exchange.upper() == 'HTX':
            adapter = HTXAdapter()
        elif exchange.upper() == 'BINANCEALPHA':
            adapter = BinanceAlphaAdapter()
        elif exchange.upper() == 'UZX':
            adapter = UZXAdapter()
        else:
            return jsonify({
                'status': 'error',
                'message': f'Unknown exchange: {exchange}'
            }), 400
        
        orderbook = adapter.fetch_orderbook(symbol, limit=5)
        
        def get_price_amount(entry):
            if isinstance(entry, dict):
                price = entry.get('price', 0)
                amount = entry.get('amount', entry.get('quantity', 0))
            elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
                price, amount = entry[0], entry[1]
            else:
                price, amount = 0, 0
            return float(price), float(amount)
        
        bid_depth = 0
        best_bid = 0
        for b in orderbook.bids[:5]:
            price, amount = get_price_amount(b)
            bid_depth += price * amount
            if best_bid == 0 and price > 0:
                best_bid = price
        
        ask_depth = 0
        best_ask = 0
        for a in orderbook.asks[:5]:
            price, amount = get_price_amount(a)
            ask_depth += price * amount
            if best_ask == 0 and price > 0:
                best_ask = price
        
        return jsonify({
            'status': 'success',
            'exchange': exchange.upper(),
            'symbol': symbol,
            'best_bid': best_bid,
            'best_ask': best_ask,
            'bid_depth': bid_depth,
            'ask_depth': ask_depth,
            'spread': ((best_ask - best_bid) / best_bid * 100) if best_bid > 0 else 0
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'exchange': exchange.upper(),
            'symbol': symbol,
            'message': str(e)
        }), 500


@app.route('/api/orderbook/<exchange>/<path:symbol>')
def get_orderbook(exchange, symbol):
    try:
        limit = request.args.get('limit', 20, type=int)
        
        if exchange.upper() == 'LBANK':
            adapter = LBankAdapter()
        elif exchange.upper() == 'HASHKEY':
            adapter = HashKeyAdapter()
        elif exchange.upper() == 'BICONOMY':
            adapter = BiconomyAdapter()
        elif exchange.upper() == 'MEXC':
            adapter = MEXCAdapter()
        elif exchange.upper() == 'BITRUE':
            adapter = BitrueAdapter()
        elif exchange.upper() == 'ASCENDEX':
            adapter = AscendEXAdapter()
        elif exchange.upper() == 'BITMART':
            adapter = BitMartAdapter()
        elif exchange.upper() == 'DEXTRADE':
            adapter = DexTradeAdapter()
        elif exchange.upper() == 'POLONIEX':
            adapter = PoloniexAdapter()
        elif exchange.upper() == 'GATEIO':
            adapter = GateIOAdapter()
        elif exchange.upper() == 'NIZA':
            adapter = NizaAdapter()
        elif exchange.upper() == 'XT':
            adapter = XTAdapter()
        elif exchange.upper() == 'COINSTORE':
            adapter = CoinstoreAdapter()
        elif exchange.upper() == 'VINDAX':
            adapter = VindaxAdapter()
        elif exchange.upper() == 'FAMEEX':
            adapter = FameEXAdapter()
        elif exchange.upper() == 'BIGONE':
            adapter = BigOneAdapter()
        elif exchange.upper() == 'P2PB2B':
            adapter = P2PB2BAdapter()
        elif exchange.upper() == 'DIGIFINEX':
            adapter = DigiFinexAdapter()
        elif exchange.upper() == 'AZBIT':
            adapter = AzbitAdapter()
        elif exchange.upper() == 'LATOKEN':
            adapter = LatokenAdapter()
        elif exchange.upper() == 'KRAKEN':
            adapter = KrakenAdapter()
        elif exchange.upper() == 'BINGX':
            adapter = BingXAdapter()
        elif exchange.upper() == 'BTSE':
            adapter = BTSEAdapter()
        elif exchange.upper() == 'WHITEBIT':
            adapter = WhiteBitAdapter()
        elif exchange.upper() == 'HTX':
            adapter = HTXAdapter()
        elif exchange.upper() == 'BINANCEALPHA':
            adapter = BinanceAlphaAdapter()
        elif exchange.upper() == 'UZX':
            adapter = UZXAdapter()
        else:
            return jsonify({
                'status': 'error',
                'message': f'Unknown exchange: {exchange}'
            }), 400
        
        orderbook = adapter.fetch_orderbook(symbol, limit)
        
        return jsonify({
            'status': 'success',
            'data': orderbook.to_dict()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/market-list/toggle', methods=['POST'])
def toggle_market_list():
    data = request.get_json()
    exchange = data.get('exchange')
    symbol = data.get('symbol')
    list_type = data.get('list_type')
    
    if not exchange or not symbol or not list_type:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    if list_type not in ['blacklist', 'whitelist', 'wallet_lock']:
        return jsonify({'status': 'error', 'message': 'Invalid list_type'}), 400
    
    if list_type == 'wallet_lock':
        whitelist_entry = MarketList.query.filter_by(
            exchange=exchange, symbol=symbol, list_type='whitelist'
        ).first()
        if not whitelist_entry:
            return jsonify({'status': 'error', 'message': 'Harus di-whitelist dulu sebelum wallet lock'}), 400
    
    existing = MarketList.query.filter_by(
        exchange=exchange,
        symbol=symbol,
        list_type=list_type
    ).first()
    
    if existing:
        db.session.delete(existing)
        if list_type == 'whitelist':
            walletlock_entry = MarketList.query.filter_by(
                exchange=exchange, symbol=symbol, list_type='wallet_lock'
            ).first()
            if walletlock_entry:
                db.session.delete(walletlock_entry)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'action': 'removed',
            'exchange': exchange,
            'symbol': symbol,
            'list_type': list_type
        })
    else:
        if list_type == 'blacklist':
            whitelist_entry = MarketList.query.filter_by(
                exchange=exchange, symbol=symbol, list_type='whitelist'
            ).first()
            if whitelist_entry:
                db.session.delete(whitelist_entry)
            walletlock_entry = MarketList.query.filter_by(
                exchange=exchange, symbol=symbol, list_type='wallet_lock'
            ).first()
            if walletlock_entry:
                db.session.delete(walletlock_entry)
        elif list_type == 'whitelist':
            blacklist_entry = MarketList.query.filter_by(
                exchange=exchange, symbol=symbol, list_type='blacklist'
            ).first()
            if blacklist_entry:
                db.session.delete(blacklist_entry)
        
        new_entry = MarketList(
            exchange=exchange,
            symbol=symbol,
            list_type=list_type
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'action': 'added',
            'exchange': exchange,
            'symbol': symbol,
            'list_type': list_type
        })


@app.route('/api/fetch/btse', methods=['POST'])
def fetch_btse():
    try:
        adapter = BTSEAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))

        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from BTSE'
        })
    except Exception as e:
        log_fetch('BTSE', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BTSE',
            'message': str(e)
        }), 500


@app.route('/api/fetch/whitebit', methods=['POST'])
def fetch_whitebit():
    try:
        adapter = WhiteBitAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))

        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from WhiteBit'
        })
    except Exception as e:
        log_fetch('WHITEBIT', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'WHITEBIT',
            'message': str(e)
        }), 500


@app.route('/api/fetch/binancealpha', methods=['POST'])
def fetch_binancealpha():
    try:
        adapter = BinanceAlphaAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))

        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} pairs from Binance Alpha'
        })
    except Exception as e:
        log_fetch('BINANCEALPHA', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'BINANCEALPHA',
            'message': str(e)
        }), 500


@app.route('/api/fetch/htx', methods=['POST'])
def fetch_htx():
    try:
        adapter = HTXAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))

        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from HTX'
        })
    except Exception as e:
        log_fetch('HTX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'HTX',
            'message': str(e)
        }), 500


@app.route('/api/fetch/uzx', methods=['POST'])
def fetch_uzx():
    try:
        adapter = UZXAdapter()
        tickers = adapter.fetch_usdt_tickers()
        save_tickers(tickers, adapter.exchange_name)
        log_fetch(adapter.exchange_name, 'success', len(tickers))

        return jsonify({
            'status': 'success',
            'exchange': adapter.exchange_name,
            'pairs_count': len(tickers),
            'message': f'Successfully fetched {len(tickers)} USDT pairs from UZX'
        })
    except Exception as e:
        log_fetch('UZX', 'error', error_message=str(e))
        return jsonify({
            'status': 'error',
            'exchange': 'UZX',
            'message': str(e)
        }), 500


_poloniex_currency_cache = {'data': None, 'ts': 0}

@app.route('/api/poloniex/currency-status')
def poloniex_currency_status():
    import time as _time
    now = _time.time()
    if _poloniex_currency_cache['data'] is not None and now - _poloniex_currency_cache['ts'] < 600:
        return jsonify({'status': 'success', 'data': _poloniex_currency_cache['data']})
    try:
        import requests as _req
        resp = _req.get(
            'https://api.poloniex.com/v2/currencies?includeMultiChainCurrencies=true',
            timeout=15
        )
        resp.raise_for_status()
        raw = resp.json()
        result = {}
        for item in raw:
            coin = item.get('coin', '').upper()
            networks = item.get('networkList', [])
            deposit = any(n.get('depositEnable', False) for n in networks)
            withdraw = any(n.get('withdrawalEnable', False) for n in networks)
            result[coin] = {'deposit': deposit, 'withdraw': withdraw}
        _poloniex_currency_cache['data'] = result
        _poloniex_currency_cache['ts'] = now
        return jsonify({'status': 'success', 'data': result})
    except Exception as e:
        logger.error(f'Poloniex currency-status error: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/scope')
def scope():
    return render_template('scope.html')


@app.route('/api/scope')
def get_scope():
    import re
    from collections import defaultdict

    exclude_leveraged = request.args.get('exclude_leveraged', 'true') == 'true'
    leveraged_pattern = re.compile(r'\d+[LSls](USDT)?$')

    all_tickers = SpotTicker.query.filter(
        SpotTicker.price.isnot(None),
        SpotTicker.price > 0,
        SpotTicker.quote_currency == 'USDT'
    ).all()

    coin_map = defaultdict(list)
    for t in all_tickers:
        if exclude_leveraged and leveraged_pattern.search(t.base_currency):
            continue
        coin_map[t.base_currency].append({
            'exchange': t.exchange,
            'last_price': float(t.price),
            'turnover': float(t.turnover_24h or 0),
            'symbol': t.symbol
        })

    result = []
    for coin, exchanges in coin_map.items():
        if len(exchanges) < 2:
            continue
        prices = [e['last_price'] for e in exchanges if e['last_price'] > 0]
        avg_price = sum(prices) / len(prices) if prices else 0
        total_turnover = sum(e['turnover'] for e in exchanges)
        result.append({
            'coin': coin,
            'symbol': f'{coin}/USDT',
            'avg_price': round(avg_price, 10),
            'exchange_count': len(exchanges),
            'total_turnover': total_turnover,
            'exchanges': exchanges
        })

    result.sort(key=lambda x: x['total_turnover'], reverse=True)
    return jsonify({'status': 'success', 'data': result})


@app.route('/api/scope/depth', methods=['POST'])
def get_scope_depth():
    from concurrent.futures import ThreadPoolExecutor, as_completed

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data'}), 400

    coin = data.get('coin', '')
    avg_price = float(data.get('avg_price', 0))
    exchanges = data.get('exchanges', [])

    if not coin or avg_price <= 0 or not exchanges:
        return jsonify({'status': 'error', 'message': 'Invalid input'}), 400

    def fetch_one(exch_info):
        exchange = exch_info['exchange']
        symbol = exch_info['symbol']
        adapter = get_adapter(exchange)
        if not adapter or not hasattr(adapter, 'fetch_orderbook'):
            return {'exchange': exchange, 'error': 'No adapter',
                    'bid_vol_above_avg': 0, 'ask_vol_below_avg': 0,
                    'best_bid': None, 'best_ask': None, 'bid_levels': [], 'ask_levels': []}
        try:
            ob = adapter.fetch_orderbook(symbol, limit=20)
            # bids/asks are [[price, amount], ...] lists
            bids = sorted(
                [{'price': float(b[0]), 'qty': float(b[1])} for b in ob.bids if len(b) >= 2],
                key=lambda x: -x['price']
            )
            asks = sorted(
                [{'price': float(a[0]), 'qty': float(a[1])} for a in ob.asks if len(a) >= 2],
                key=lambda x: x['price']
            )

            # Best bid = highest bid on this exchange (top of book)
            best_bid = bids[0]['price'] if bids else None
            bid_vol_usd = sum(b['price'] * b['qty'] for b in bids[:5])
            bid_levels = [{'price': b['price'], 'qty': b['qty'],
                           'usd': round(b['price'] * b['qty'], 2)} for b in bids[:6]]

            # Best ask = lowest ask on this exchange (top of book)
            best_ask = asks[0]['price'] if asks else None
            ask_vol_usd = sum(a['price'] * a['qty'] for a in asks[:5])
            ask_levels = [{'price': a['price'], 'qty': a['qty'],
                           'usd': round(a['price'] * a['qty'], 2)} for a in asks[:6]]

            return {
                'exchange': exchange,
                'best_bid': best_bid,
                'bid_vol_above_avg': round(bid_vol_usd, 2),
                'bid_levels': bid_levels,
                'best_ask': best_ask,
                'ask_vol_below_avg': round(ask_vol_usd, 2),
                'ask_levels': ask_levels,
                'error': None
            }
        except Exception as e:
            logger.error(f'Scope depth {exchange}/{coin}: {e}')
            return {'exchange': exchange, 'error': str(e),
                    'bid_vol_above_avg': 0, 'ask_vol_below_avg': 0,
                    'best_bid': None, 'best_ask': None, 'bid_levels': [], 'ask_levels': []}

    results = []
    with ThreadPoolExecutor(max_workers=min(len(exchanges), 8)) as executor:
        futures = {executor.submit(fetch_one, e): e for e in exchanges}
        for future in as_completed(futures):
            r = future.result()
            if r:
                results.append(r)

    fee_pct = float(data.get('fee_pct', 0.4))

    sell_opps = [r for r in results if r['best_bid'] is not None]
    buy_opps  = [r for r in results if r['best_ask'] is not None]
    best_sell = max(sell_opps, key=lambda x: x['best_bid']) if sell_opps else None
    cross_buy_opps = [r for r in buy_opps if not best_sell or r['exchange'] != best_sell['exchange']]
    best_buy = min(cross_buy_opps, key=lambda x: x['best_ask']) if cross_buy_opps else None

    real_spread = None
    net_spread  = None
    if best_sell and best_buy and best_buy['best_ask'] > 0:
        real_spread = round(
            (best_sell['best_bid'] - best_buy['best_ask']) / best_buy['best_ask'] * 100, 3
        )
        net_spread = round(real_spread - fee_pct, 3)

    results.sort(key=lambda x: x['bid_vol_above_avg'], reverse=True)

    return jsonify({
        'status': 'success',
        'coin': coin,
        'avg_price': avg_price,
        'results': results,
        'best_sell': best_sell,
        'best_buy': best_buy,
        'real_spread': real_spread,
        'net_spread': net_spread,
        'fee_pct': fee_pct
    })


@app.route('/api/scope/fetch-all', methods=['POST'])
def get_scope_fetch_all():
    from concurrent.futures import ThreadPoolExecutor, as_completed

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data'}), 400

    coins = data.get('coins', [])
    if not coins:
        return jsonify({'status': 'error', 'message': 'No coins provided'}), 400

    def fetch_coin_depth(coin_info):
        coin = coin_info['coin']
        avg_price = float(coin_info['avg_price'])
        exchanges = coin_info['exchanges']

        def fetch_one(exch_info):
            exchange = exch_info['exchange']
            symbol = exch_info['symbol']
            adapter = get_adapter(exchange)
            if not adapter or not hasattr(adapter, 'fetch_orderbook'):
                return {'exchange': exchange, 'error': 'No adapter',
                        'bid_vol_above_avg': 0, 'ask_vol_below_avg': 0,
                        'best_bid': None, 'best_ask': None, 'bid_levels': [], 'ask_levels': []}
            try:
                ob = adapter.fetch_orderbook(symbol, limit=20)
                # bids/asks are [[price, amount], ...] lists
                bids = sorted(
                    [{'price': float(b[0]), 'qty': float(b[1])} for b in ob.bids if len(b) >= 2],
                    key=lambda x: -x['price']
                )
                asks = sorted(
                    [{'price': float(a[0]), 'qty': float(a[1])} for a in ob.asks if len(a) >= 2],
                    key=lambda x: x['price']
                )
                # Best bid = highest bid on this exchange (top of book)
                best_bid = bids[0]['price'] if bids else None
                bid_vol_usd = sum(b['price'] * b['qty'] for b in bids[:5])
                bid_levels = [{'price': b['price'], 'qty': b['qty'],
                               'usd': round(b['price'] * b['qty'], 2)} for b in bids[:6]]
                # Best ask = lowest ask on this exchange (top of book)
                best_ask = asks[0]['price'] if asks else None
                ask_vol_usd = sum(a['price'] * a['qty'] for a in asks[:5])
                ask_levels = [{'price': a['price'], 'qty': a['qty'],
                               'usd': round(a['price'] * a['qty'], 2)} for a in asks[:6]]
                return {
                    'exchange': exchange,
                    'best_bid': best_bid,
                    'bid_vol_above_avg': round(bid_vol_usd, 2),
                    'bid_levels': bid_levels,
                    'best_ask': best_ask,
                    'ask_vol_below_avg': round(ask_vol_usd, 2),
                    'ask_levels': ask_levels,
                    'error': None
                }
            except Exception as e:
                logger.error(f'Scope depth {exchange}/{coin}: {e}')
                return {'exchange': exchange, 'error': str(e),
                        'bid_vol_above_avg': 0, 'ask_vol_below_avg': 0,
                        'best_bid': None, 'best_ask': None, 'bid_levels': [], 'ask_levels': []}

        results = []
        with ThreadPoolExecutor(max_workers=min(len(exchanges), 6)) as ex:
            futs = {ex.submit(fetch_one, e): e for e in exchanges}
            for fut in as_completed(futs):
                r = fut.result()
                if r:
                    results.append(r)

        fee_pct = float(data.get('fee_pct', 0.4))

        sell_opps = [r for r in results if r['best_bid'] is not None]
        buy_opps  = [r for r in results if r['best_ask'] is not None]
        best_sell = max(sell_opps, key=lambda x: x['best_bid']) if sell_opps else None
        cross_buy_opps = [r for r in buy_opps if not best_sell or r['exchange'] != best_sell['exchange']]
        best_buy = min(cross_buy_opps, key=lambda x: x['best_ask']) if cross_buy_opps else None

        real_spread = None
        net_spread  = None
        if best_sell and best_buy and best_buy['best_ask'] > 0:
            real_spread = round(
                (best_sell['best_bid'] - best_buy['best_ask']) / best_buy['best_ask'] * 100, 3
            )
            net_spread = round(real_spread - fee_pct, 3)

        results.sort(key=lambda x: x['bid_vol_above_avg'], reverse=True)

        return {
            'coin': coin,
            'avg_price': avg_price,
            'results': results,
            'best_sell': best_sell,
            'best_buy': best_buy,
            'real_spread': real_spread,
            'net_spread': net_spread,
            'fee_pct': fee_pct
        }

    all_results = {}
    with ThreadPoolExecutor(max_workers=min(len(coins), 10)) as executor:
        future_map = {executor.submit(fetch_coin_depth, c): c['coin'] for c in coins}
        for future in as_completed(future_map):
            coin_name = future_map[future]
            try:
                result = future.result()
                all_results[coin_name] = result
            except Exception as e:
                logger.error(f'fetch-all coin {coin_name}: {e}')
                all_results[coin_name] = {
                    'coin': coin_name, 'avg_price': 0,
                    'results': [], 'best_sell': None, 'best_buy': None,
                    'real_spread': None, 'net_spread': None, 'fee_pct': 0.4
                }

    return jsonify({'status': 'success', 'data': all_results})


@app.route('/market-fetch')
def market_fetch_page():
    return render_template('market_fetch.html')


@app.route('/api/market-fetch/status')
def market_fetch_status():
    from sqlalchemy import func
    ticker_counts = db.session.query(
        SpotTicker.exchange, func.count(SpotTicker.id)
    ).group_by(SpotTicker.exchange).all()
    snap_data = db.session.query(
        OrderbookSnapshot.exchange,
        func.count(OrderbookSnapshot.id),
        func.max(OrderbookSnapshot.fetched_at)
    ).group_by(OrderbookSnapshot.exchange).all()

    ticker_map = {e: c for e, c in ticker_counts}
    snap_map = {e: {'count': c, 'last_fetched': ts.isoformat() if ts else None}
                for e, c, ts in snap_data}
    all_exchanges = sorted(set(list(ticker_map.keys()) + list(snap_map.keys())))
    result = []
    for exc in all_exchanges:
        result.append({
            'exchange': exc,
            'ticker_count': ticker_map.get(exc, 0),
            'snapshot_count': snap_map.get(exc, {}).get('count', 0),
            'last_fetched': snap_map.get(exc, {}).get('last_fetched')
        })
    return jsonify({'status': 'success', 'data': result})


@app.route('/api/market-fetch/<exchange>', methods=['POST'])
def do_market_fetch(exchange):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    exch_upper = exchange.upper()
    adapter = get_adapter(exch_upper)
    if not adapter:
        return jsonify({'status': 'error', 'message': f'No adapter for {exch_upper}'}), 404
    if not hasattr(adapter, 'fetch_orderbook'):
        return jsonify({'status': 'error', 'message': f'{exch_upper} does not support orderbook'}), 400

    # Only fetch tickers that have actual trading volume (skip dead markets)
    tickers = SpotTicker.query.filter_by(exchange=exch_upper).filter(
        SpotTicker.volume_24h > 0
    ).all()
    if not tickers:
        # Fallback: try all tickers if none have volume data
        tickers = SpotTicker.query.filter_by(exchange=exch_upper).all()
    if not tickers:
        return jsonify({'status': 'error', 'message': 'Tidak ada ticker. Fetch harga dulu di halaman utama.'}), 400

    import time as _time

    def fetch_ob(symbol):
        for attempt in range(2):  # 1 retry on 429
            try:
                ob = adapter.fetch_orderbook(symbol, limit=5)
                bids = [[float(b[0]), float(b[1])] for b in ob.bids[:5] if len(b) >= 2]
                asks = [[float(a[0]), float(a[1])] for a in ob.asks[:5] if len(a) >= 2]
                if not bids or not asks:
                    return symbol, None, None, None, None, 'empty orderbook'
                best_bid = bids[0][0]
                best_ask = asks[0][0]
                return symbol, bids, asks, best_bid, best_ask, None
            except Exception as e:
                err_str = str(e)
                if '429' in err_str and attempt == 0:
                    _time.sleep(1.5)  # back off and retry once on rate limit
                    continue
                return symbol, None, None, None, None, err_str
        return symbol, None, None, None, None, 'max retries exceeded'

    success = 0
    failed = 0
    start = datetime.utcnow()
    snap_updates = []

    # 8 workers — enough parallelism without triggering rate limits
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_ob, t.symbol): t.symbol for t in tickers}
        for future in as_completed(futures):
            symbol, bids, asks, best_bid, best_ask, err = future.result()
            if err:
                failed += 1
            else:
                snap_updates.append((symbol, bids, asks, best_bid, best_ask))
                success += 1

    # Bulk upsert
    from sqlalchemy.orm.attributes import flag_modified
    now = datetime.utcnow()
    existing = {s.symbol: s for s in
                OrderbookSnapshot.query.filter_by(exchange=exch_upper).all()}
    for symbol, bids, asks, best_bid, best_ask in snap_updates:
        if symbol in existing:
            snap = existing[symbol]
            snap.bids = bids
            snap.asks = asks
            snap.best_bid = best_bid
            snap.best_ask = best_ask
            snap.fetched_at = now
            flag_modified(snap, 'bids')
            flag_modified(snap, 'asks')
        else:
            snap = OrderbookSnapshot(
                exchange=exch_upper, symbol=symbol,
                bids=bids, asks=asks,
                best_bid=best_bid, best_ask=best_ask,
                fetched_at=now
            )
            db.session.add(snap)
    db.session.commit()

    duration = round((datetime.utcnow() - start).total_seconds(), 1)
    return jsonify({
        'status': 'success', 'exchange': exch_upper,
        'success': success, 'failed': failed, 'duration': duration
    })


STALE_THRESHOLD_SEC = 300  # 5 minutes — snapshots older than this are flagged


@app.route('/api/scope/from-db', methods=['POST'])
def get_scope_from_db():
    from collections import defaultdict
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data'}), 400
    coins = data.get('coins', [])
    if not coins:
        return jsonify({'status': 'error', 'message': 'No coins'}), 400

    fee_pct = float(data.get('fee_pct', 0.4))
    coin_map = {c['coin']: float(c['avg_price']) for c in coins}
    symbols_needed = [f"{coin}/USDT" for coin in coin_map]

    # Query ALL snapshots for needed symbols — ignore frontend exchange list entirely
    # This ensures we always use the latest DB state regardless of when the page was loaded
    all_snaps = OrderbookSnapshot.query.filter(
        OrderbookSnapshot.symbol.in_(symbols_needed)
    ).all()

    # Group snapshots by symbol
    snaps_by_symbol = defaultdict(list)
    for s in all_snaps:
        snaps_by_symbol[s.symbol].append(s)

    latest_ts = max((s.fetched_at for s in all_snaps), default=None)
    now = datetime.utcnow()

    all_results = {}
    for coin, avg_price in coin_map.items():
        symbol = f"{coin}/USDT"
        snap_list = snaps_by_symbol.get(symbol, [])

        results = []
        for snap in snap_list:
            if not snap.bids or not snap.asks:
                continue
            try:
                bids = sorted(
                    [{'price': float(b[0]), 'qty': float(b[1])} for b in snap.bids if len(b) >= 2],
                    key=lambda x: -x['price']
                )
                asks = sorted(
                    [{'price': float(a[0]), 'qty': float(a[1])} for a in snap.asks if len(a) >= 2],
                    key=lambda x: x['price']
                )
            except (TypeError, IndexError):
                continue
            if not bids or not asks:
                continue
            best_bid = bids[0]['price']
            bid_vol_usd = sum(b['price'] * b['qty'] for b in bids[:5])
            bid_levels = [{'price': b['price'], 'qty': b['qty'],
                           'usd': round(b['price'] * b['qty'], 2)} for b in bids[:6]]
            best_ask = asks[0]['price']
            ask_vol_usd = sum(a['price'] * a['qty'] for a in asks[:5])
            ask_levels = [{'price': a['price'], 'qty': a['qty'],
                           'usd': round(a['price'] * a['qty'], 2)} for a in asks[:6]]
            snap_age = round((now - snap.fetched_at).total_seconds()) if snap.fetched_at else None
            is_stale = snap_age is not None and snap_age > STALE_THRESHOLD_SEC
            results.append({
                'exchange': snap.exchange,
                'best_bid': best_bid,
                'bid_vol_above_avg': round(bid_vol_usd, 2),
                'bid_levels': bid_levels,
                'best_ask': best_ask,
                'ask_vol_below_avg': round(ask_vol_usd, 2),
                'ask_levels': ask_levels,
                'snap_age_sec': snap_age,
                'is_stale': is_stale,
                'error': None
            })

        # Require ≥2 exchanges with actual snapshot data
        if len(results) < 2:
            best_sell = best_buy = real_spread = net_spread = None
        else:
            sell_opps = [r for r in results if r['best_bid'] is not None]
            buy_opps  = [r for r in results if r['best_ask'] is not None]
            best_sell = max(sell_opps, key=lambda x: x['best_bid']) if sell_opps else None
            cross_buy = [r for r in buy_opps if not best_sell or r['exchange'] != best_sell['exchange']]
            best_buy  = min(cross_buy, key=lambda x: x['best_ask']) if cross_buy else None

            real_spread = None
            net_spread  = None
            if best_sell and best_buy and best_buy['best_ask'] > 0:
                real_spread = round(
                    (best_sell['best_bid'] - best_buy['best_ask']) / best_buy['best_ask'] * 100, 3
                )
                net_spread = round(real_spread - fee_pct, 3)

        results.sort(key=lambda x: x['bid_vol_above_avg'], reverse=True)
        all_results[coin] = {
            'coin': coin, 'avg_price': avg_price,
            'results': results,
            'best_sell': best_sell, 'best_buy': best_buy,
            'real_spread': real_spread,
            'net_spread': net_spread,
            'fee_pct': fee_pct
        }

    return jsonify({
        'status': 'success',
        'data': all_results,
        'source': 'db',
        'snapshot_time': latest_ts.isoformat() if latest_ts else None
    })


@app.route('/arbitrage')
def arbitrage():
    return render_template('arbitrage.html')


@app.route('/api/arbitrage')
def get_arbitrage():
    import re
    from sqlalchemy import func

    exclude_leveraged = request.args.get('exclude_leveraged', 'true') == 'true'
    leveraged_pattern = re.compile(r'\d+[LSls](USDT)?$')

    arb_blacklist = {e.symbol for e in MarketList.query.filter_by(exchange='ARB', list_type='blacklist').all()}
    arb_wishlist = {e.symbol for e in MarketList.query.filter_by(exchange='ARB', list_type='whitelist').all()}

    subq = db.session.query(
        SpotTicker.symbol,
        func.count(SpotTicker.exchange).label('exchange_count')
    ).filter(
        SpotTicker.price.isnot(None),
        SpotTicker.price > 0
    ).group_by(SpotTicker.symbol).having(
        func.count(SpotTicker.exchange) >= 2
    ).subquery()

    tickers = db.session.query(SpotTicker).join(
        subq, SpotTicker.symbol == subq.c.symbol
    ).filter(
        SpotTicker.price.isnot(None),
        SpotTicker.price > 0
    ).all()

    grouped = {}
    for t in tickers:
        if exclude_leveraged and leveraged_pattern.search(t.base_currency):
            continue
        if t.symbol not in grouped:
            grouped[t.symbol] = []
        grouped[t.symbol].append(t)

    results = []
    for symbol, entries in grouped.items():
        valid_entries = [e for e in entries if e.price and e.price > 0]
        if len(valid_entries) < 2:
            continue

        exchange_count = len(valid_entries)
        max_entry = max(valid_entries, key=lambda e: e.price)
        min_entry = min(valid_entries, key=lambda e: e.price)

        spread_pct = ((max_entry.price - min_entry.price) / min_entry.price) * 100

        total_turnover = sum(e.turnover_24h for e in valid_entries if e.turnover_24h)

        exchange_list = sorted([{
            'exchange': e.exchange,
            'price': e.price,
            'turnover_24h': e.turnover_24h,
            'change_24h': e.change_24h
        } for e in valid_entries], key=lambda x: x['price'], reverse=True)

        results.append({
            'symbol': symbol,
            'base_currency': valid_entries[0].base_currency,
            'exchange_count': exchange_count,
            'max_price': max_entry.price,
            'max_exchange': max_entry.exchange,
            'max_turnover': max_entry.turnover_24h,
            'min_price': min_entry.price,
            'min_exchange': min_entry.exchange,
            'min_turnover': min_entry.turnover_24h,
            'spread_pct': round(spread_pct, 4),
            'total_turnover': total_turnover,
            'exchanges': exchange_list,
            'is_blacklisted': symbol in arb_blacklist,
            'is_wishlisted': symbol in arb_wishlist
        })

    results.sort(key=lambda x: x['spread_pct'], reverse=True)

    return jsonify({'status': 'success', 'data': results, 'count': len(results)})


@app.route('/exchange-focus')
def exchange_focus():
    return render_template('exchange_focus.html')


@app.route('/api/exchange-focus')
def get_exchange_focus():
    exchange = request.args.get('exchange', 'MEXC').upper()

    arb_blacklist = {e.symbol for e in MarketList.query.filter_by(exchange='ARB', list_type='blacklist').all()}

    anchor_tickers = SpotTicker.query.filter_by(exchange=exchange).filter(
        SpotTicker.price.isnot(None),
        SpotTicker.price > 0
    ).all()

    if not anchor_tickers:
        return jsonify({'status': 'success', 'anchor': exchange, 'data': [], 'count': 0})

    anchor_map = {t.symbol: t for t in anchor_tickers}

    other_tickers = SpotTicker.query.filter(
        SpotTicker.symbol.in_(list(anchor_map.keys())),
        SpotTicker.exchange != exchange,
        SpotTicker.price.isnot(None),
        SpotTicker.price > 0
    ).all()

    others_by_symbol = {}
    for t in other_tickers:
        others_by_symbol.setdefault(t.symbol, []).append(t)

    results = []
    for symbol, anchor_t in anchor_map.items():
        others = others_by_symbol.get(symbol, [])

        other_list = []
        best_spread = 0.0

        for o in others:
            if anchor_t.price and anchor_t.price > 0:
                diff_pct = ((o.price - anchor_t.price) / anchor_t.price) * 100
            else:
                diff_pct = 0.0
            abs_diff = abs(diff_pct)
            if abs_diff > best_spread:
                best_spread = abs_diff
            other_list.append({
                'exchange': o.exchange,
                'price': o.price,
                'turnover_24h': o.turnover_24h,
                'diff_pct': round(diff_pct, 4)
            })

        other_list.sort(key=lambda x: x['price'], reverse=True)

        results.append({
            'symbol': symbol,
            'base_currency': anchor_t.base_currency,
            'anchor_price': anchor_t.price,
            'anchor_turnover': anchor_t.turnover_24h,
            'other_exchanges': other_list,
            'other_count': len(other_list),
            'best_spread_pct': round(best_spread, 4),
            'is_blacklisted': symbol in arb_blacklist
        })

    results.sort(key=lambda x: x['best_spread_pct'], reverse=True)

    return jsonify({'status': 'success', 'anchor': exchange, 'data': results, 'count': len(results)})


@app.route('/api/market-list')
def get_market_list():
    list_type = request.args.get('type', None)
    
    query = MarketList.query
    if list_type:
        query = query.filter_by(list_type=list_type)
    
    entries = query.all()
    return jsonify({
        'status': 'success',
        'data': [e.to_dict() for e in entries]
    })
