let allTickers = [];
let symbolMap = {};
let currentSort = { column: 'symbol', direction: 'asc' };

document.addEventListener('DOMContentLoaded', function() {
    loadTickers();
    loadStatus();
    setupHeaderSorting();
});

async function fetchData(exchange) {
    const btn = document.getElementById(`btn-${exchange}`);
    btn.classList.add('loading');
    btn.disabled = true;
    
    try {
        const response = await fetch(`/api/fetch/${exchange}`, {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.status === 'success') {
            showToast(`${data.message}`, 'success');
            await loadTickers();
            await loadStatus();
        } else {
            showToast(`Error: ${data.message}`, 'error');
        }
    } catch (error) {
        showToast(`Failed to fetch data: ${error.message}`, 'error');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

async function loadTickers() {
    try {
        const response = await fetch('/api/tickers');
        const data = await response.json();
        
        if (data.status === 'success') {
            allTickers = data.data;
            buildSymbolMap();
            filterTable();
        }
    } catch (error) {
        console.error('Failed to load tickers:', error);
    }
}

function buildSymbolMap() {
    symbolMap = {};
    allTickers.forEach(t => {
        if (!symbolMap[t.symbol]) {
            symbolMap[t.symbol] = {};
        }
        symbolMap[t.symbol][t.exchange] = t;
    });
}

function getPeerExchangeData(ticker) {
    const symbolData = symbolMap[ticker.symbol];
    if (!symbolData) return null;
    
    for (const exchange in symbolData) {
        if (exchange !== ticker.exchange) {
            return symbolData[exchange];
        }
    }
    return null;
}

async function loadStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        updateStatusDisplay('lbank', data.lbank);
        updateStatusDisplay('hashkey', data.hashkey);
    } catch (error) {
        console.error('Failed to load status:', error);
    }
}

function updateStatusDisplay(exchange, status) {
    const statusItem = document.getElementById(`status-${exchange}`);
    if (!statusItem) return;
    
    const badge = statusItem.querySelector('.status-badge');
    const count = statusItem.querySelector('.status-count');
    
    if (status.status === 'never' || !status.last_fetch) {
        badge.className = 'status-badge never';
        badge.textContent = 'Never fetched';
    } else if (status.status === 'success') {
        badge.className = 'status-badge success';
        const time = formatRelativeTime(new Date(status.last_fetch));
        badge.textContent = time;
    } else {
        badge.className = 'status-badge error';
        badge.textContent = 'Error';
    }
    
    count.textContent = `${status.pairs_count} pairs`;
}

function formatRelativeTime(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
}

function setupHeaderSorting() {
    const headers = document.querySelectorAll('th[data-sort]');
    headers.forEach(th => {
        th.addEventListener('click', () => {
            const column = th.dataset.sort;
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }
            updateSortIndicators();
            filterTable();
        });
    });
}

function updateSortIndicators() {
    const headers = document.querySelectorAll('th[data-sort]');
    headers.forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
        if (th.dataset.sort === currentSort.column) {
            th.classList.add(currentSort.direction === 'asc' ? 'sort-asc' : 'sort-desc');
        }
    });
}

function renderTable(tickers) {
    const tbody = document.getElementById('ticker-body');
    const countEl = document.getElementById('ticker-count');
    
    if (tickers.length === 0) {
        tbody.innerHTML = `
            <tr class="empty-row">
                <td colspan="9">
                    <div class="empty-state">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                        </svg>
                        <p>No data yet. Click a fetch button to load exchange data.</p>
                    </div>
                </td>
            </tr>
        `;
        countEl.textContent = '0 pairs displayed';
        return;
    }
    
    tbody.innerHTML = tickers.map(t => {
        const exchangeClass = t.exchange.toLowerCase();
        const changeClass = t.change_24h > 0 ? 'positive' : t.change_24h < 0 ? 'negative' : 'neutral';
        const changeArrow = t.change_24h > 0 ? '↑' : t.change_24h < 0 ? '↓' : '−';
        
        const peer = getPeerExchangeData(t);
        let peerDataHtml = '<span class="no-peer">−</span>';
        
        if (peer && peer.price && t.price) {
            const peerExchangeClass = peer.exchange.toLowerCase();
            const priceDiff = ((peer.price - t.price) / t.price * 100);
            const diffClass = priceDiff > 0.01 ? 'positive' : priceDiff < -0.01 ? 'negative' : 'neutral';
            const diffSign = priceDiff > 0 ? '+' : '';
            
            peerDataHtml = `
                <div class="peer-data">
                    <span class="peer-exchange ${peerExchangeClass}">${peer.exchange}</span>
                    <span class="peer-price">${formatPrice(peer.price)}</span>
                    <span class="peer-diff ${diffClass}">(${diffSign}${priceDiff.toFixed(2)}%)</span>
                    <button class="orderbook-btn-sm" onclick="showOrderbook('${peer.exchange}', '${peer.symbol}')">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 6h16M4 12h16M4 18h16"/>
                        </svg>
                    </button>
                </div>
            `;
        }
        
        return `
            <tr>
                <td class="td-exchange">
                    <span class="exchange-badge ${exchangeClass}">${t.exchange}</span>
                </td>
                <td class="td-symbol">${t.symbol}</td>
                <td class="td-price">${formatPrice(t.price)}</td>
                <td class="td-volume">${formatVolume(t.volume_24h)}</td>
                <td class="td-high">${formatPrice(t.high_24h)}</td>
                <td class="td-low">${formatPrice(t.low_24h)}</td>
                <td class="td-change ${changeClass}">
                    <span class="change-arrow">${changeArrow}</span>${formatChange(t.change_24h)}%
                </td>
                <td class="td-action">
                    <button class="orderbook-btn" onclick="showOrderbook('${t.exchange}', '${t.symbol}')">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 6h16M4 12h16M4 18h16"/>
                        </svg>
                        View
                    </button>
                </td>
                <td class="td-peer">${peerDataHtml}</td>
            </tr>
        `;
    }).join('');
    
    countEl.textContent = `${tickers.length} pairs displayed`;
}

function formatPrice(price) {
    if (price === null || price === undefined) return '−';
    if (price === 0) return '0.00';
    
    if (price < 0.0001) {
        return price.toExponential(4);
    } else if (price < 1) {
        return price.toFixed(6);
    } else if (price < 100) {
        return price.toFixed(4);
    } else if (price < 10000) {
        return price.toFixed(2);
    } else {
        return price.toLocaleString('en-US', { maximumFractionDigits: 2 });
    }
}

function formatVolume(volume) {
    if (volume === null || volume === undefined) return '−';
    if (volume === 0) return '0';
    
    if (volume >= 1e9) {
        return (volume / 1e9).toFixed(2) + 'B';
    } else if (volume >= 1e6) {
        return (volume / 1e6).toFixed(2) + 'M';
    } else if (volume >= 1e3) {
        return (volume / 1e3).toFixed(2) + 'K';
    } else {
        return volume.toFixed(2);
    }
}

function formatChange(change) {
    if (change === null || change === undefined) return '0.00';
    return Math.abs(change).toFixed(2);
}

function filterTable() {
    const exchangeFilter = document.getElementById('exchange-filter').value;
    const searchValue = document.getElementById('search-input').value.toLowerCase();
    
    let filtered = allTickers;
    
    if (exchangeFilter !== 'all') {
        filtered = filtered.filter(t => t.exchange === exchangeFilter);
    }
    
    if (searchValue) {
        filtered = filtered.filter(t => 
            t.symbol.toLowerCase().includes(searchValue) ||
            t.base_currency.toLowerCase().includes(searchValue)
        );
    }
    
    filtered = sortTickersByColumn(filtered);
    renderTable(filtered);
}

function sortTickersByColumn(tickers) {
    const sorted = [...tickers];
    const { column, direction } = currentSort;
    const mult = direction === 'asc' ? 1 : -1;
    
    switch (column) {
        case 'symbol':
            sorted.sort((a, b) => mult * a.symbol.localeCompare(b.symbol));
            break;
        case 'price':
            sorted.sort((a, b) => mult * ((a.price || 0) - (b.price || 0)));
            break;
        case 'volume':
            sorted.sort((a, b) => mult * ((a.volume_24h || 0) - (b.volume_24h || 0)));
            break;
        case 'high':
            sorted.sort((a, b) => mult * ((a.high_24h || 0) - (b.high_24h || 0)));
            break;
        case 'low':
            sorted.sort((a, b) => mult * ((a.low_24h || 0) - (b.low_24h || 0)));
            break;
        case 'change':
            sorted.sort((a, b) => mult * ((a.change_24h || 0) - (b.change_24h || 0)));
            break;
    }
    
    return sorted;
}

function showToast(message, type) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

async function showOrderbook(exchange, symbol) {
    const modal = document.getElementById('orderbook-modal');
    const title = document.getElementById('modal-title');
    const asksList = document.getElementById('asks-list');
    const bidsList = document.getElementById('bids-list');
    
    title.textContent = `Orderbook: ${symbol} (${exchange})`;
    asksList.innerHTML = '<div class="loading-spinner">Loading...</div>';
    bidsList.innerHTML = '<div class="loading-spinner">Loading...</div>';
    modal.classList.add('show');
    
    try {
        const response = await fetch(`/api/orderbook/${exchange}/${symbol}?limit=10`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const orderbook = data.data;
            
            asksList.innerHTML = orderbook.asks.slice(0, 10).map(([price, qty]) => `
                <div class="orderbook-row ask">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatQuantity(qty)}</span>
                </div>
            `).join('') || '<div class="no-data">No asks</div>';
            
            bidsList.innerHTML = orderbook.bids.slice(0, 10).map(([price, qty]) => `
                <div class="orderbook-row bid">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatQuantity(qty)}</span>
                </div>
            `).join('') || '<div class="no-data">No bids</div>';
        } else {
            asksList.innerHTML = `<div class="error-msg">${data.message}</div>`;
            bidsList.innerHTML = `<div class="error-msg">${data.message}</div>`;
        }
    } catch (error) {
        asksList.innerHTML = `<div class="error-msg">Failed to load orderbook</div>`;
        bidsList.innerHTML = `<div class="error-msg">Failed to load orderbook</div>`;
    }
}

function closeOrderbookModal() {
    const modal = document.getElementById('orderbook-modal');
    modal.classList.remove('show');
}

function formatQuantity(qty) {
    if (qty === null || qty === undefined) return '−';
    if (qty >= 1e6) return (qty / 1e6).toFixed(2) + 'M';
    if (qty >= 1e3) return (qty / 1e3).toFixed(2) + 'K';
    if (qty >= 1) return qty.toFixed(4);
    return qty.toFixed(6);
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeOrderbookModal();
    }
});

document.getElementById('orderbook-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeOrderbookModal();
    }
});
