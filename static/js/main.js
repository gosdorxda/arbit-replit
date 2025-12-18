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
            return `https://www.biconomy.com/exchange/${pairUpper}`;
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
        case 'XT':
            return `https://www.xt.com/en/trade/${pair}`;
        case 'COINSTORE':
            return `https://www.coinstore.com/spot/${base}USDT`;
        case 'VINDAX':
            return `https://vindax.com/exchange-base.html?symbol=${base}_USDT`;
        default:
            return '#';
    }
}

$(document).ready(function() {
    initTheme();
    initDataTable();
    loadStatus();
    
    $('#exchange-filter').on('change', function() {
        updateExchangeColumnVisibility();
        dataTable.ajax.reload();
    });
    
    $('#multi-exchange-filter').on('change', function() {
        dataTable.ajax.reload();
    });
    
    $('#list-filter').on('change', function() {
        dataTable.ajax.reload();
    });
    
    updateExchangeColumnVisibility();
});

function initDataTable() {
    dataTable = $('#ticker-table').DataTable({
        processing: true,
        serverSide: true,
        autoWidth: false,
        ajax: {
            url: '/api/tickers',
            data: function(d) {
                d.exchange = $('#exchange-filter').val();
                d.multi_exchange = $('#multi-exchange-filter').is(':checked');
                d.list_filter = $('#list-filter').val();
            }
        },
        columns: [
            { 
                data: 'exchange',
                className: 'td-exchange',
                render: function(data) {
                    const exchangeClass = data.toLowerCase();
                    return `<span class="exchange-badge ${exchangeClass}">${data}</span>`;
                },
                orderable: true
            },
            { 
                data: null,
                className: 'td-symbol',
                render: function(data) {
                    const url = getExchangeUrl(data.exchange, data.symbol);
                    return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="symbol-link">${data.symbol}</a>`;
                },
                orderable: true
            },
            { 
                data: 'change_24h',
                className: 'td-change',
                render: function(data) {
                    const changeClass = data > 0 ? 'change-positive' : data < 0 ? 'change-negative' : 'change-neutral';
                    const changeArrow = data > 0 ? '↑' : data < 0 ? '↓' : '−';
                    return `<span class="${changeClass}"><span class="change-arrow">${changeArrow}</span>${formatChange(data)}%</span>`;
                },
                orderable: true
            },
            { 
                data: null,
                className: 'td-volume',
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
                className: 'td-action',
                render: function(data) {
                    return `<button class="orderbook-btn" onclick="showOrderbook('${data.exchange}', '${data.symbol}', this)">
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
                className: 'td-price',
                render: function(data) {
                    return `<span class="price-value">${formatPrice(data)}</span>`;
                },
                orderable: true
            },
            {
                data: 'peers',
                className: 'td-peer',
                render: function(peers, type, row) {
                    if (!peers || peers.length === 0) {
                        return '<span class="no-peer">−</span>';
                    }
                    
                    let html = '<div class="peer-list">';
                    peers.forEach(peer => {
                        if (!peer.price) return;
                        const peerExchangeClass = peer.exchange.toLowerCase();
                        const peerVolume = peer.turnover_24h ? formatVolume(peer.turnover_24h) : '−';
                        const peerUrl = getExchangeUrl(peer.exchange, peer.symbol);
                        
                        html += `
                            <div class="peer-data">
                                <span class="peer-price">${formatPrice(peer.price)}</span>
                                <button class="orderbook-btn-sm" onclick="showOrderbook2('${peer.exchange}', '${peer.symbol}', this)">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 6h16M4 12h16M4 18h16"/>
                                    </svg>
                                </button>
                                <span class="peer-volume">${peerVolume}</span>
                                <a href="${peerUrl}" target="_blank" rel="noopener noreferrer" class="peer-exchange ${peerExchangeClass}">${peer.exchange}</a>
                            </div>
                        `;
                    });
                    html += '</div>';
                    return html;
                },
                orderable: false
            },
            {
                data: null,
                className: 'td-list',
                render: function(data) {
                    const blacklistChecked = data.is_blacklisted ? 'checked' : '';
                    const whitelistChecked = data.is_whitelisted ? 'checked' : '';
                    return `
                        <div class="list-checkboxes">
                            <label class="list-cb blacklist-cb" title="Blacklist">
                                <input type="checkbox" ${blacklistChecked} onchange="toggleMarketList('${data.exchange}', '${data.symbol}', 'blacklist', this)">
                                <span class="cb-icon">⛔</span>
                            </label>
                            <label class="list-cb whitelist-cb" title="Whitelist">
                                <input type="checkbox" ${whitelistChecked} onchange="toggleMarketList('${data.exchange}', '${data.symbol}', 'whitelist', this)">
                                <span class="cb-icon">⭐</span>
                            </label>
                        </div>
                    `;
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
        drawCallback: function(settings) {
            const json = settings.json;
            if (json) {
                $('#current-pairs').text(json.recordsTotal || 0);
                $('#comparable-pairs').text(json.comparablePairs || 0);
            }
        }
    });
}

function updateExchangeColumnVisibility() {
    const selectedExchange = $('#exchange-filter').val();
    if (dataTable) {
        dataTable.column(0).visible(selectedExchange === '');
    }
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
        updateStatusDisplay('xt', data.xt);
        updateStatusDisplay('coinstore', data.coinstore);
        updateStatusDisplay('vindax', data.vindax);
        
        let totalMarkets = 0;
        const exchanges = ['lbank', 'hashkey', 'biconomy', 'mexc', 'bitrue', 'ascendex', 'bitmart', 'dextrade', 'poloniex', 'gateio', 'niza', 'xt', 'coinstore', 'vindax'];
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

let activeRow = null;
let activeRow2 = null;

async function showOrderbook(exchange, symbol, btnElement) {
    const modal = document.getElementById('orderbook-modal');
    const modalTitle = document.getElementById('modal-title');
    const asksList = document.getElementById('asks-list');
    const bidsList = document.getElementById('bids-list');
    const spreadDivider = document.getElementById('spread-divider');
    
    if (activeRow) {
        activeRow.classList.remove('row-active');
    }
    if (btnElement) {
        activeRow = btnElement.closest('tr');
        if (activeRow) {
            activeRow.classList.add('row-active');
        }
    }
    
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
    if (activeRow) {
        activeRow.classList.remove('row-active');
        activeRow = null;
    }
}

async function showOrderbook2(exchange, symbol, btnElement) {
    const modal = document.getElementById('orderbook-modal2');
    const modalTitle = document.getElementById('modal-title2');
    const asksList = document.getElementById('asks-list2');
    const bidsList = document.getElementById('bids-list2');
    const spreadDivider = document.getElementById('spread-divider2');
    
    if (activeRow2) {
        activeRow2.classList.remove('row-active');
    }
    if (btnElement) {
        activeRow2 = btnElement.closest('tr');
        if (activeRow2) {
            activeRow2.classList.add('row-active');
        }
    }
    
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
            
            const allAsks = orderbook.asks.map(parseEntry).sort((a, b) => a.price - b.price);
            const asksToShow = allAsks.slice(0, 15).reverse();
            asksList.innerHTML = asksToShow.map(({ price, amount }) => `
                <div class="orderbook-row ask">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                </div>
            `).join('');
            
            asksList.scrollTop = asksList.scrollHeight;
            
            const allBids = orderbook.bids.map(parseEntry).sort((a, b) => b.price - a.price);
            const bidsToShow = allBids.slice(0, 15);
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

function closeOrderbookModal2() {
    const modal = document.getElementById('orderbook-modal2');
    modal.classList.remove('show');
    if (activeRow2) {
        activeRow2.classList.remove('row-active');
        activeRow2 = null;
    }
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeOrderbookModal();
        closeOrderbookModal2();
    }
});

async function toggleMarketList(exchange, symbol, listType, checkbox) {
    try {
        const response = await fetch('/api/market-list/toggle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                exchange: exchange,
                symbol: symbol,
                list_type: listType
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const row = checkbox.closest('tr');
            const otherType = listType === 'blacklist' ? 'whitelist' : 'blacklist';
            const otherCheckbox = row.querySelector(`.${otherType}-cb input`);
            if (otherCheckbox && data.action === 'added') {
                otherCheckbox.checked = false;
            }
            
            const actionText = data.action === 'added' ? 'ditambahkan ke' : 'dihapus dari';
            const listName = listType === 'blacklist' ? 'Blacklist' : 'Whitelist';
            showToast(`${symbol} ${actionText} ${listName}`, 'success');
        } else {
            checkbox.checked = !checkbox.checked;
            showToast(data.message || 'Gagal mengubah list', 'error');
        }
    } catch (error) {
        checkbox.checked = !checkbox.checked;
        showToast('Gagal mengubah list: ' + error.message, 'error');
    }
}

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

function makeDraggable(modalId) {
    const modal = document.getElementById(modalId);
    const modalContent = modal.querySelector('.modal-content');
    const header = modal.querySelector('.modal-header');
    
    let isDragging = false;
    let startX, startY, initialX, initialY;
    
    header.addEventListener('mousedown', function(e) {
        if (e.target.classList.contains('modal-close')) return;
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        
        const transform = window.getComputedStyle(modalContent).transform;
        if (transform && transform !== 'none') {
            const matrix = new DOMMatrix(transform);
            initialX = matrix.m41;
            initialY = matrix.m42;
        } else {
            initialX = 0;
            initialY = 0;
        }
        
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });
    
    function onMouseMove(e) {
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        modalContent.style.transform = `translate(${initialX + dx}px, ${initialY + dy}px)`;
    }
    
    function onMouseUp() {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    makeDraggable('orderbook-modal');
    makeDraggable('orderbook-modal2');
});
