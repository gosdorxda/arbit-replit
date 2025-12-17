let dataTable = null;

function getExchangeUrl(exchange, symbol) {
    const pair = symbol.replace('/', '_').toLowerCase();
    const pairUpper = symbol.replace('/', '_');
    const base = symbol.split('/')[0];
    
    switch(exchange.toUpperCase()) {
        case 'LBANK':
            return `https://www.lbank.com/trade/${pair}`;
        case 'HASHKEY':
            return `https://global.hashkey.com/en-US/spot/${symbol.replace('/', '-')}`;
        case 'BICONOMY':
            return `https://www.biconomy.com/exchange?coin=${pairUpper}`;
        case 'MEXC':
            return `https://www.mexc.com/exchange/${pairUpper}`;
        case 'BITRUE':
            return `https://www.bitrue.com/trade/${pair}`;
        case 'ASCENDEX':
            return `https://ascendex.com/en/cashtrade-spottrading/usdt/${base.toLowerCase()}`;
        case 'BITMART':
            return `https://www.bitmart.com/trade/en-US?symbol=${pairUpper}`;
        case 'DEXTRADE':
            return `https://dex-trade.com/spot/trading/${symbol.replace('/', '')}?interface=classic`;
        case 'POLONIEX':
            return `https://poloniex.com/trade/${base}_USDT`;
        case 'GATEIO':
            return `https://www.gate.io/trade/${pairUpper}`;
        case 'NIZA':
            return `https://niza.io/trade/${pairUpper}`;
        default:
            return '#';
    }
}

$(document).ready(function() {
    initTheme();
    initDataTable();
    loadStatus();
    
    $('#exchange-filter').on('change', function() {
        dataTable.ajax.reload();
    });
    
    $('#multi-exchange-filter').on('change', function() {
        dataTable.ajax.reload();
    });
});

function initDataTable() {
    dataTable = $('#ticker-table').DataTable({
        processing: true,
        serverSide: true,
        ajax: {
            url: '/api/tickers',
            data: function(d) {
                d.exchange = $('#exchange-filter').val();
                d.multi_exchange = $('#multi-exchange-filter').is(':checked');
            }
        },
        columns: [
            { 
                data: 'exchange',
                render: function(data) {
                    const exchangeClass = data.toLowerCase();
                    return `<span class="exchange-badge ${exchangeClass}">${data}</span>`;
                },
                orderable: true
            },
            { 
                data: null,
                render: function(data) {
                    const url = getExchangeUrl(data.exchange, data.symbol);
                    return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="symbol-link">${data.symbol}</a>`;
                },
                orderable: true
            },
            { 
                data: 'change_24h',
                render: function(data) {
                    const changeClass = data > 0 ? 'change-positive' : data < 0 ? 'change-negative' : 'change-neutral';
                    const changeArrow = data > 0 ? '↑' : data < 0 ? '↓' : '−';
                    return `<span class="${changeClass}"><span class="change-arrow">${changeArrow}</span>${formatChange(data)}%</span>`;
                },
                orderable: true
            },
            { 
                data: null,
                render: function(data) {
                    const turnover = data.turnover_24h;
                    const exchangeCount = data.exchange_count || 1;
                    
                    if (exchangeCount > 1) {
                        let totalVolume = turnover || 0;
                        if (data.peers) {
                            data.peers.forEach(p => {
                                totalVolume += (p.turnover_24h || 0);
                            });
                        }
                        return `<div class="volume-info"><span class="volume-own">${formatVolume(turnover)}</span><span class="volume-total" title="Total across ${exchangeCount} exchanges">Σ ${formatVolume(totalVolume)}</span></div>`;
                    }
                    return formatVolume(turnover);
                },
                orderable: true
            },
            {
                data: null,
                render: function(data) {
                    return `<button class="orderbook-btn" onclick="showOrderbook('${data.exchange}', '${data.symbol}')">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 6h16M4 12h16M4 18h16"/>
                        </svg>
                        View
                    </button>`;
                },
                orderable: false
            },
            { 
                data: 'price',
                render: function(data) {
                    return `<span class="price-value">${formatPrice(data)}</span>`;
                },
                orderable: true
            },
            {
                data: 'peers',
                render: function(peers, type, row) {
                    if (!peers || peers.length === 0) {
                        return '<span class="no-peer">−</span>';
                    }
                    
                    let html = '<div class="peer-list">';
                    peers.forEach(peer => {
                        if (!peer.price) return;
                        const peerExchangeClass = peer.exchange.toLowerCase();
                        const priceDiff = ((peer.price - row.price) / row.price * 100);
                        const diffClass = priceDiff > 0.01 ? 'change-positive' : priceDiff < -0.01 ? 'change-negative' : 'change-neutral';
                        const diffSign = priceDiff > 0 ? '+' : '';
                        const peerVolume = peer.turnover_24h ? formatVolume(peer.turnover_24h) : '−';
                        const peerUrl = getExchangeUrl(peer.exchange, peer.symbol);
                        
                        html += `
                            <div class="peer-data">
                                <a href="${peerUrl}" target="_blank" rel="noopener noreferrer" class="peer-exchange ${peerExchangeClass}">${peer.exchange}</a>
                                <span class="peer-price">${formatPrice(peer.price)}</span>
                                <span class="peer-diff ${diffClass}">(${diffSign}${priceDiff.toFixed(2)}%)</span>
                                <span class="peer-volume">Vol: ${peerVolume}</span>
                                <button class="orderbook-btn-sm" onclick="showOrderbook('${peer.exchange}', '${peer.symbol}')">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 6h16M4 12h16M4 18h16"/>
                                    </svg>
                                </button>
                            </div>
                        `;
                    });
                    html += '</div>';
                    return html;
                },
                orderable: false
            }
        ],
        order: [[1, 'asc']],
        pageLength: 50,
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        language: {
            processing: '<div class="dt-loading">Loading...</div>',
            emptyTable: 'No data yet. Click a fetch button to load exchange data.',
            zeroRecords: 'No matching records found'
        },
        dom: '<"dt-top"lf>rt<"dt-bottom"ip>',
        drawCallback: function() {
        }
    });
}

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
            dataTable.ajax.reload();
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

async function loadStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        updateStatusDisplay('lbank', data.lbank);
        updateStatusDisplay('hashkey', data.hashkey);
        updateStatusDisplay('biconomy', data.biconomy);
        updateStatusDisplay('mexc', data.mexc);
        updateStatusDisplay('bitrue', data.bitrue);
        updateStatusDisplay('ascendex', data.ascendex);
        updateStatusDisplay('bitmart', data.bitmart);
        updateStatusDisplay('dextrade', data.dextrade);
        updateStatusDisplay('poloniex', data.poloniex);
        updateStatusDisplay('gateio', data.gateio);
        updateStatusDisplay('niza', data.niza);
        
        let totalMarkets = 0;
        const exchanges = ['lbank', 'hashkey', 'biconomy', 'mexc', 'bitrue', 'ascendex', 'bitmart', 'dextrade', 'poloniex', 'gateio', 'niza'];
        exchanges.forEach(ex => {
            if (data[ex] && data[ex].pairs_count) {
                totalMarkets += data[ex].pairs_count;
            }
        });
        
        const totalMarketsEl = document.getElementById('total-markets');
        if (totalMarketsEl) {
            totalMarketsEl.textContent = totalMarkets.toLocaleString();
        }
    } catch (error) {
        console.error('Failed to load status:', error);
    }
}

function updateStatusDisplay(exchange, status) {
    const btn = document.getElementById(`btn-${exchange}`);
    if (!btn) return;
    
    const timeEl = btn.querySelector('.btn-time');
    const pairsEl = btn.querySelector('.btn-pairs');
    
    if (status.status === 'never' || !status.last_fetch) {
        timeEl.textContent = 'Never fetched';
        timeEl.className = 'btn-time never';
    } else if (status.status === 'success') {
        const time = formatRelativeTime(new Date(status.last_fetch));
        timeEl.textContent = time;
        timeEl.className = 'btn-time success';
    } else {
        timeEl.textContent = 'Error';
        timeEl.className = 'btn-time error';
    }
    
    pairsEl.textContent = `${status.pairs_count} pairs`;
}

function formatRelativeTime(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);
    
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
}

function formatPrice(price) {
    if (price === null || price === undefined) return '−';
    if (price === 0) return '0.00';
    
    if (price >= 100000) {
        return price.toLocaleString('en-US', { maximumFractionDigits: 2 });
    } else if (price >= 1000) {
        return price.toFixed(2);
    } else if (price >= 1) {
        return price.toFixed(4);
    } else if (price >= 0.0001) {
        return price.toFixed(6);
    } else {
        const str = price.toFixed(20);
        const match = str.match(/^0\.(0*)([1-9]\d*)/);
        if (match) {
            const leadingZeros = match[1].length;
            const significantDigits = Math.min(8, match[2].length);
            return price.toFixed(leadingZeros + significantDigits);
        }
        return price.toFixed(10);
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

async function showOrderbook(exchange, symbol) {
    const modal = document.getElementById('orderbook-modal');
    const modalTitle = document.getElementById('modal-title');
    const asksList = document.getElementById('asks-list');
    const bidsList = document.getElementById('bids-list');
    const spreadDivider = document.getElementById('spread-divider');
    
    modalTitle.textContent = `${symbol} Orderbook (${exchange})`;
    asksList.innerHTML = '<div class="orderbook-loading">Loading...</div>';
    bidsList.innerHTML = '';
    spreadDivider.textContent = '−';
    
    modal.classList.add('show');
    
    try {
        const response = await fetch(`/api/orderbook/${exchange}/${encodeURIComponent(symbol)}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const orderbook = data.data;
            
            const parseEntry = (item) => {
                if (Array.isArray(item)) {
                    return { price: parseFloat(item[0]), amount: parseFloat(item[1]) };
                }
                return { price: parseFloat(item.price), amount: parseFloat(item.amount) };
            };
            
            // Parse all, sort ascending to get lowest asks first, take 15 closest to spread, then reverse for display
            const allAsks = orderbook.asks.map(parseEntry).sort((a, b) => a.price - b.price);
            const asksToShow = allAsks.slice(0, 15).reverse(); // reverse so highest at top, lowest at bottom (near spread)
            asksList.innerHTML = asksToShow.map(({ price, amount }) => `
                <div class="orderbook-row ask">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                </div>
            `).join('');
            
            // Auto-scroll asks to bottom so lowest price (near spread) is visible
            asksList.scrollTop = asksList.scrollHeight;
            
            // Parse all, sort descending to get highest bids first, take 15 closest to spread
            const allBids = orderbook.bids.map(parseEntry).sort((a, b) => b.price - a.price);
            const bidsToShow = allBids.slice(0, 15); // highest at top (near spread), lowest at bottom
            bidsList.innerHTML = bidsToShow.map(({ price, amount }) => `
                <div class="orderbook-row bid">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                </div>
            `).join('');
            
            if (allAsks.length > 0 && allBids.length > 0) {
                const lowestAsk = allAsks[0].price;
                const highestBid = allBids[0].price;
                const spread = ((lowestAsk - highestBid) / lowestAsk * 100).toFixed(4);
                spreadDivider.textContent = `Spread: ${spread}%`;
            }
        } else {
            asksList.innerHTML = `<div class="orderbook-error">${data.message}</div>`;
        }
    } catch (error) {
        asksList.innerHTML = `<div class="orderbook-error">Failed to load orderbook</div>`;
    }
}

function closeOrderbookModal() {
    const modal = document.getElementById('orderbook-modal');
    modal.classList.remove('show');
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeOrderbookModal();
    }
});

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    const savedFont = localStorage.getItem('font') || 'inter';
    document.documentElement.setAttribute('data-font', savedFont);
    updateFontIcon(savedFont);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const iconSun = document.querySelector('.icon-sun');
    const iconMoon = document.querySelector('.icon-moon');
    
    if (theme === 'dark') {
        iconSun.style.display = 'block';
        iconMoon.style.display = 'none';
    } else {
        iconSun.style.display = 'none';
        iconMoon.style.display = 'block';
    }
}

const fonts = ['inter', 'roboto', 'opensans'];
const fontNames = { 'inter': 'In', 'roboto': 'Ro', 'opensans': 'Os' };

function toggleFont() {
    const currentFont = document.documentElement.getAttribute('data-font') || 'inter';
    const currentIndex = fonts.indexOf(currentFont);
    const nextIndex = (currentIndex + 1) % fonts.length;
    const newFont = fonts[nextIndex];
    
    document.documentElement.setAttribute('data-font', newFont);
    localStorage.setItem('font', newFont);
    updateFontIcon(newFont);
}

function updateFontIcon(font) {
    const fontIcon = document.querySelector('.font-icon');
    if (fontIcon) {
        fontIcon.textContent = fontNames[font] || 'Aa';
    }
}
