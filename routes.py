from datetime import datetime
from flask import render_template, jsonify, request
from app import app, db
from models import SpotTicker, FetchLog
from adapters import LBankAdapter, HashKeyAdapter, BiconomyAdapter, MEXCAdapter, BitrueAdapter, AscendEXAdapter


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


@app.route('/api/tickers')
def get_tickers():
    draw = request.args.get('draw', 1, type=int)
    start = request.args.get('start', 0, type=int)
    length = request.args.get('length', 50, type=int)
    search_value = request.args.get('search[value]', '', type=str)
    exchange_filter = request.args.get('exchange', '', type=str)
    multi_exchange = request.args.get('multi_exchange', 'false', type=str) == 'true'
    order_column = request.args.get('order[0][column]', '1', type=str)
    order_dir = request.args.get('order[0][dir]', 'asc', type=str)
    
    column_map = {
        '0': SpotTicker.exchange,
        '1': SpotTicker.symbol,
        '2': SpotTicker.change_24h,
        '3': SpotTicker.turnover_24h,
        '4': None,
        '5': SpotTicker.price,
        '6': None
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
    
    total_records = SpotTicker.query.count()
    filtered_records = query.count()
    
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
        data.append(ticker_dict)
    
    return jsonify({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
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
    
    lbank_count = SpotTicker.query.filter_by(exchange='LBANK').count()
    hashkey_count = SpotTicker.query.filter_by(exchange='HASHKEY').count()
    biconomy_count = SpotTicker.query.filter_by(exchange='BICONOMY').count()
    mexc_count = SpotTicker.query.filter_by(exchange='MEXC').count()
    bitrue_count = SpotTicker.query.filter_by(exchange='BITRUE').count()
    ascendex_count = SpotTicker.query.filter_by(exchange='ASCENDEX').count()
    
    return jsonify({
        'lbank': {
            'last_fetch': lbank_log.fetched_at.isoformat() if lbank_log else None,
            'status': lbank_log.status if lbank_log else 'never',
            'pairs_count': lbank_count
        },
        'hashkey': {
            'last_fetch': hashkey_log.fetched_at.isoformat() if hashkey_log else None,
            'status': hashkey_log.status if hashkey_log else 'never',
            'pairs_count': hashkey_count
        },
        'biconomy': {
            'last_fetch': biconomy_log.fetched_at.isoformat() if biconomy_log else None,
            'status': biconomy_log.status if biconomy_log else 'never',
            'pairs_count': biconomy_count
        },
        'mexc': {
            'last_fetch': mexc_log.fetched_at.isoformat() if mexc_log else None,
            'status': mexc_log.status if mexc_log else 'never',
            'pairs_count': mexc_count
        },
        'bitrue': {
            'last_fetch': bitrue_log.fetched_at.isoformat() if bitrue_log else None,
            'status': bitrue_log.status if bitrue_log else 'never',
            'pairs_count': bitrue_count
        },
        'ascendex': {
            'last_fetch': ascendex_log.fetched_at.isoformat() if ascendex_log else None,
            'status': ascendex_log.status if ascendex_log else 'never',
            'pairs_count': ascendex_count
        }
    })


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
