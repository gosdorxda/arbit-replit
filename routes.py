from datetime import datetime
from flask import render_template, jsonify, request
from app import app, db
from models import SpotTicker, FetchLog, MarketList
from adapters import LBankAdapter, HashKeyAdapter, BiconomyAdapter, MEXCAdapter, BitrueAdapter, AscendEXAdapter, BitMartAdapter, DexTradeAdapter, PoloniexAdapter, GateIOAdapter, NizaAdapter, XTAdapter, CoinstoreAdapter, VindaxAdapter, FameEXAdapter, BigOneAdapter, P2PB2BAdapter, DigiFinexAdapter, AzbitAdapter, LatokenAdapter


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


@app.route('/api/tickers')
def get_tickers():
    draw = request.args.get('draw', 1, type=int)
    start = request.args.get('start', 0, type=int)
    length = request.args.get('length', 50, type=int)
    search_value = request.args.get('search[value]', '', type=str)
    exchange_filter = request.args.get('exchange', '', type=str)
    multi_exchange = request.args.get('multi_exchange', 'false', type=str) == 'true'
    list_filter = request.args.get('list_filter', '', type=str)
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
        symbol_map[t.symbol][t.exchange] = t.to_dict()
    
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
    
    exchanges = ['LBANK', 'HASHKEY', 'BICONOMY', 'MEXC', 'BITRUE', 'ASCENDEX', 
                 'BITMART', 'DEXTRADE', 'POLONIEX', 'GATEIO', 'NIZA', 'XT', 
                 'COINSTORE', 'VINDAX', 'FAMEEX', 'BIGONE', 'P2PB2B', 'DIGIFINEX', 'AZBIT', 'LATOKEN']
    
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
        else:
            return jsonify({
                'status': 'error',
                'message': f'Unknown exchange: {exchange}'
            }), 400
        
        orderbook = adapter.fetch_orderbook(symbol, limit=5)
        
        bid_depth = sum(b['price'] * b['amount'] for b in orderbook.bids[:5])
        ask_depth = sum(a['price'] * a['amount'] for a in orderbook.asks[:5])
        
        best_bid = orderbook.bids[0]['price'] if orderbook.bids else 0
        best_ask = orderbook.asks[0]['price'] if orderbook.asks else 0
        
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
