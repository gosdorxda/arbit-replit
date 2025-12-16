from datetime import datetime, timezone, timedelta
from app import db

JAKARTA_TZ = timezone(timedelta(hours=7))

def jakarta_now():
    return datetime.now(JAKARTA_TZ).replace(tzinfo=None)


class SpotTicker(db.Model):
    __tablename__ = 'spot_tickers'
    
    id = db.Column(db.Integer, primary_key=True)
    exchange = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(50), nullable=False)
    base_currency = db.Column(db.String(20), nullable=False)
    quote_currency = db.Column(db.String(20), nullable=False, default='USDT')
    price = db.Column(db.Float, nullable=True)
    volume_24h = db.Column(db.Float, nullable=True)
    high_24h = db.Column(db.Float, nullable=True)
    low_24h = db.Column(db.Float, nullable=True)
    change_24h = db.Column(db.Float, nullable=True)
    turnover_24h = db.Column(db.Float, nullable=True)
    fetched_at = db.Column(db.DateTime, nullable=False, default=jakarta_now)
    
    __table_args__ = (
        db.UniqueConstraint('exchange', 'symbol', name='unique_exchange_symbol'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'exchange': self.exchange,
            'symbol': self.symbol,
            'base_currency': self.base_currency,
            'quote_currency': self.quote_currency,
            'price': self.price,
            'volume_24h': self.volume_24h,
            'high_24h': self.high_24h,
            'low_24h': self.low_24h,
            'change_24h': self.change_24h,
            'turnover_24h': self.turnover_24h,
            'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None
        }


class FetchLog(db.Model):
    __tablename__ = 'fetch_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    exchange = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    pairs_count = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text, nullable=True)
    fetched_at = db.Column(db.DateTime, nullable=False, default=jakarta_now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'exchange': self.exchange,
            'status': self.status,
            'pairs_count': self.pairs_count,
            'error_message': self.error_message,
            'fetched_at': self.fetched_at.isoformat() if self.fetched_at else None
        }
