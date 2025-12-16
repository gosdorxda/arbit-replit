from datetime import datetime
from flask import render_template, jsonify, request
from app import app, db
from models import SpotTicker, FetchLog
from adapters import LBankAdapter, HashKeyAdapter


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


@app.route('/api/tickers')
def get_tickers():
    tickers = SpotTicker.query.order_by(SpotTicker.exchange, SpotTicker.symbol).all()
    return jsonify({
        'status': 'success',
        'count': len(tickers),
        'data': [t.to_dict() for t in tickers]
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
    
    lbank_count = SpotTicker.query.filter_by(exchange='LBANK').count()
    hashkey_count = SpotTicker.query.filter_by(exchange='HASHKEY').count()
    
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
