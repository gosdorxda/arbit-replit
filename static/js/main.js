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
        case 'FAMEEX':
            return `https://www.fameex.com/en-US/trade/${base.toLowerCase()}-usdt`;
        case 'BIGONE':
            return `https://big.one/en/trade/${base}-USDT`;
        case 'P2PB2B':
            return `https://p2pb2b.com/trade/${base}_USDT`;
        case 'DIGIFINEX':
            return `https://www.digifinex.com/en-ww/trade/USDT/${base}`;
        case 'AZBIT':
            return `https://azbit.com/exchange/${base}_USDT`;
        case 'LATOKEN':
            return `https://latoken.com/exchange/${base}_USDT`;
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
                    
                    const sortedPeers = [...peers].filter(p => p.price).sort((a, b) => b.price - a.price);
                    
                    let html = '<div class="peer-list">';
                    sortedPeers.forEach(peer => {
                        if (!peer.price) return;
                        const peerExchangeClass = peer.exchange.toLowerCase();
                        const peerVolume = peer.turnover_24h ? formatVolume(peer.turnover_24h) : '−';
                        const peerUrl = getExchangeUrl(peer.exchange, peer.symbol);
                        const peerId = `depth-${peer.exchange}-${peer.symbol.replace('/', '-')}`.toLowerCase();
                        
                        html += `
                            <div class="peer-data" id="${peerId}">
                                <span class="peer-price">${formatPrice(peer.price)}</span>
                                <button class="orderbook-btn-sm" onclick="showOrderbook2('${peer.exchange}', '${peer.symbol}', this)">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 6h16M4 12h16M4 18h16"/>
                                    </svg>
                                </button>
                                <span class="peer-volume">${peerVolume}</span>
                                <span class="depth-box" onclick="loadDepth('${peer.exchange}', '${peer.symbol}', '${peerId}')" title="Click for depth">
                                    <span class="db-row db-ask"><span class="db-label">Ask:</span><span class="db-price">−</span><span class="db-vol">−</span></span>
                                    <span class="db-row db-bid"><span class="db-label">Bid:</span><span class="db-price">−</span><span class="db-vol">−</span></span>
                                </span>
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
                    const walletLockChecked = data.is_wallet_locked ? 'checked' : '';
                    const walletLockVisible = data.is_whitelisted ? '' : 'style="display:none"';
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
                            <label class="list-cb walletlock-cb" title="Wallet Lock" ${walletLockVisible}>
                                <input type="checkbox" ${walletLockChecked} onchange="toggleMarketList('${data.exchange}', '${data.symbol}', 'wallet_lock', this)">
                                <span class="cb-icon">🔒</span>
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
        updateStatusDisplay('fameex', data.fameex);
        updateStatusDisplay('bigone', data.bigone);
        updateStatusDisplay('p2pb2b', data.p2pb2b);
        updateStatusDisplay('digifinex', data.digifinex);
        updateStatusDisplay('azbit', data.azbit);
        updateStatusDisplay('latoken', data.latoken);
        
        let totalMarkets = 0;
        const exchanges = ['lbank', 'hashkey', 'biconomy', 'mexc', 'bitrue', 'ascendex', 'bitmart', 'dextrade', 'poloniex', 'gateio', 'niza', 'xt', 'coinstore', 'vindax', 'fameex', 'bigone', 'p2pb2b', 'digifinex', 'azbit', 'latoken'];
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
    const listEl = btn.querySelector('.btn-list');
    
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
    
    if (listEl) {
        const wl = status.whitelist_count || 0;
        const bl = status.blacklist_count || 0;
        const lk = status.walletlock_count || 0;
        if (wl > 0 || bl > 0 || lk > 0) {
            let html = '';
            if (wl > 0) html += `<span class="wl-count" title="Whitelist">⭐${wl}</span>`;
            if (bl > 0) html += `<span class="bl-count" title="Blacklist">⛔${bl}</span>`;
            if (lk > 0) html += `<span class="lk-count" title="Wallet Lock">🔒${lk}</span>`;
            listEl.innerHTML = html;
            listEl.style.display = 'flex';
        } else {
            listEl.style.display = 'none';
        }
    }
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
            let askCumulative = 0;
            // Calculate cumulative from bottom (near spread) to top
            const askTotals = [];
            for (let i = asksToShow.length - 1; i >= 0; i--) {
                askCumulative += asksToShow[i].price * asksToShow[i].amount;
                askTotals[i] = askCumulative;
            }
            asksList.innerHTML = asksToShow.map(({ price, amount }, idx) => `
                <div class="orderbook-row ask">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                    <span class="ob-total">${formatVolume(askTotals[idx])}</span>
                </div>
            `).join('');
            
            // Auto-scroll asks to bottom so lowest price (near spread) is visible
            asksList.scrollTop = asksList.scrollHeight;
            
            // Parse all, sort descending to get highest bids first, take 15 closest to spread
            const allBids = orderbook.bids.map(parseEntry).sort((a, b) => b.price - a.price);
            const bidsToShow = allBids.slice(0, 15); // highest at top (near spread), lowest at bottom
            let bidCumulative = 0;
            bidsList.innerHTML = bidsToShow.map(({ price, amount }) => {
                bidCumulative += price * amount;
                return `
                <div class="orderbook-row bid">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                    <span class="ob-total">${formatVolume(bidCumulative)}</span>
                </div>
            `}).join('');
            
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
            let askCumulative2 = 0;
            const askTotals2 = [];
            for (let i = asksToShow.length - 1; i >= 0; i--) {
                askCumulative2 += asksToShow[i].price * asksToShow[i].amount;
                askTotals2[i] = askCumulative2;
            }
            asksList.innerHTML = asksToShow.map(({ price, amount }, idx) => `
                <div class="orderbook-row ask">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                    <span class="ob-total">${formatVolume(askTotals2[idx])}</span>
                </div>
            `).join('');
            
            asksList.scrollTop = asksList.scrollHeight;
            
            const allBids = orderbook.bids.map(parseEntry).sort((a, b) => b.price - a.price);
            const bidsToShow = allBids.slice(0, 15);
            let bidCumulative2 = 0;
            bidsList.innerHTML = bidsToShow.map(({ price, amount }) => {
                bidCumulative2 += price * amount;
                return `
                <div class="orderbook-row bid">
                    <span class="ob-price">${formatPrice(price)}</span>
                    <span class="ob-qty">${formatVolume(amount)}</span>
                    <span class="ob-total">${formatVolume(bidCumulative2)}</span>
                </div>
            `}).join('');
            
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
            
            if (listType === 'blacklist' && data.action === 'added') {
                const whitelistCb = row.querySelector('.whitelist-cb input');
                const walletlockCb = row.querySelector('.walletlock-cb input');
                const walletlockLabel = row.querySelector('.walletlock-cb');
                if (whitelistCb) whitelistCb.checked = false;
                if (walletlockCb) walletlockCb.checked = false;
                if (walletlockLabel) walletlockLabel.style.display = 'none';
            } else if (listType === 'whitelist') {
                const blacklistCb = row.querySelector('.blacklist-cb input');
                const walletlockLabel = row.querySelector('.walletlock-cb');
                if (blacklistCb && data.action === 'added') blacklistCb.checked = false;
                if (walletlockLabel) {
                    walletlockLabel.style.display = data.action === 'added' ? '' : 'none';
                    if (data.action === 'removed') {
                        const walletlockCb = row.querySelector('.walletlock-cb input');
                        if (walletlockCb) walletlockCb.checked = false;
                    }
                }
            }
            
            const actionText = data.action === 'added' ? 'ditambahkan ke' : 'dihapus dari';
            const listNames = {'blacklist': 'Blacklist', 'whitelist': 'Whitelist', 'wallet_lock': 'Wallet Lock'};
            const listName = listNames[listType] || listType;
            showToast(`${symbol} ${actionText} ${listName}`, 'success');
            
            loadStatus();
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
    
    const savedFontSize = localStorage.getItem('fontsize') || 'medium';
    document.documentElement.setAttribute('data-fontsize', savedFontSize);
    updateFontSizeIcon(savedFontSize);
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

const fonts = ['inter', 'roboto', 'poppins'];
const fontNames = { 'inter': 'In', 'roboto': 'Ro', 'poppins': 'Po' };

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

const fontSizes = ['small', 'medium', 'large'];
const fontSizeLabels = { 'small': 'S', 'medium': 'M', 'large': 'L' };

function toggleFontSize() {
    const currentSize = document.documentElement.getAttribute('data-fontsize') || 'medium';
    const currentIndex = fontSizes.indexOf(currentSize);
    const nextIndex = (currentIndex + 1) % fontSizes.length;
    const newSize = fontSizes[nextIndex];
    
    document.documentElement.setAttribute('data-fontsize', newSize);
    localStorage.setItem('fontsize', newSize);
    updateFontSizeIcon(newSize);
}

function updateFontSizeIcon(size) {
    const fontSizeIcon = document.querySelector('.fontsize-icon');
    if (fontSizeIcon) {
        fontSizeIcon.textContent = fontSizeLabels[size] || 'M';
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
    initDepthAutoLoader();
});

const loadedDepthIds = new Set();
const depthLoadQueue = [];
let isProcessingQueue = false;

function initDepthAutoLoader() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const depthBox = entry.target;
                const peerId = depthBox.closest('.peer-data')?.id;
                if (peerId && !loadedDepthIds.has(peerId)) {
                    const parts = peerId.replace('depth-', '').split('-');
                    const exchange = parts[0].toUpperCase();
                    const symbol = parts.slice(1).join('/').replace(/-/g, '/').toUpperCase();
                    queueDepthLoad(exchange, symbol, peerId);
                }
            }
        });
    }, {
        root: null,
        rootMargin: '50px',
        threshold: 0.1
    });
    
    const tableBody = document.querySelector('#ticker-table tbody');
    if (tableBody) {
        const mutationObserver = new MutationObserver(() => {
            document.querySelectorAll('.depth-box:not(.observed)').forEach(box => {
                box.classList.add('observed');
                observer.observe(box);
            });
        });
        mutationObserver.observe(tableBody, { childList: true, subtree: true });
    }
    
    document.querySelectorAll('.depth-box').forEach(box => {
        box.classList.add('observed');
        observer.observe(box);
    });
}

function queueDepthLoad(exchange, symbol, elementId) {
    if (loadedDepthIds.has(elementId)) return;
    loadedDepthIds.add(elementId);
    depthLoadQueue.push({ exchange, symbol, elementId });
    processDepthQueue();
}

async function processDepthQueue() {
    if (isProcessingQueue || depthLoadQueue.length === 0) return;
    isProcessingQueue = true;
    
    while (depthLoadQueue.length > 0) {
        const batch = depthLoadQueue.splice(0, 3);
        await Promise.all(batch.map(item => 
            loadDepthSilent(item.exchange, item.symbol, item.elementId)
        ));
        if (depthLoadQueue.length > 0) {
            await new Promise(resolve => setTimeout(resolve, 200));
        }
    }
    
    isProcessingQueue = false;
}

async function loadDepthSilent(exchange, symbol, elementId) {
    const container = document.getElementById(elementId);
    if (!container) return;
    
    const depthBox = container.querySelector('.depth-box');
    const askRow = container.querySelector('.db-ask');
    const bidRow = container.querySelector('.db-bid');
    if (!askRow || !bidRow) return;
    
    const askPrice = askRow.querySelector('.db-price');
    const askVol = askRow.querySelector('.db-vol');
    const bidPrice = bidRow.querySelector('.db-price');
    const bidVol = bidRow.querySelector('.db-vol');
    
    try {
        const response = await fetch(`/api/depth/${exchange}/${encodeURIComponent(symbol)}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const askDepthClass = getDepthColor(data.ask_depth);
            const bidDepthClass = getDepthColor(data.bid_depth);
            
            askPrice.textContent = formatPrice(data.best_ask);
            askVol.textContent = formatDepthValue(data.ask_depth);
            askVol.className = `db-vol ${askDepthClass}`;
            
            bidPrice.textContent = formatPrice(data.best_bid);
            bidVol.textContent = formatDepthValue(data.bid_depth);
            bidVol.className = `db-vol ${bidDepthClass}`;
            
            depthBox.classList.add('loaded');
            depthBox.title = `Spread: ${data.spread.toFixed(2)}%`;
        }
    } catch (e) {
        // Silent fail for auto-load
    }
}

function formatDepthValue(value) {
    if (value >= 1000000) {
        return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
        return (value / 1000).toFixed(1) + 'K';
    }
    return value.toFixed(0);
}

function getDepthColor(depth) {
    if (depth >= 100000) return 'depth-high';
    if (depth >= 10000) return 'depth-medium';
    if (depth >= 1000) return 'depth-low';
    return 'depth-minimal';
}

async function loadDepth(exchange, symbol, elementId) {
    const container = document.getElementById(elementId);
    if (!container) return;
    
    const depthBox = container.querySelector('.depth-box');
    const askRow = container.querySelector('.db-ask');
    const bidRow = container.querySelector('.db-bid');
    const askPrice = askRow.querySelector('.db-price');
    const askVol = askRow.querySelector('.db-vol');
    const bidPrice = bidRow.querySelector('.db-price');
    const bidVol = bidRow.querySelector('.db-vol');
    
    askPrice.textContent = '...';
    askVol.textContent = '...';
    bidPrice.textContent = '...';
    bidVol.textContent = '...';
    
    try {
        const response = await fetch(`/api/depth/${exchange}/${encodeURIComponent(symbol)}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            const askDepthClass = getDepthColor(data.ask_depth);
            const bidDepthClass = getDepthColor(data.bid_depth);
            
            askPrice.textContent = formatPrice(data.best_ask);
            askVol.textContent = formatDepthValue(data.ask_depth);
            askVol.className = `db-vol ${askDepthClass}`;
            
            bidPrice.textContent = formatPrice(data.best_bid);
            bidVol.textContent = formatDepthValue(data.bid_depth);
            bidVol.className = `db-vol ${bidDepthClass}`;
            
            depthBox.classList.add('loaded');
            depthBox.title = `Spread: ${data.spread.toFixed(2)}%`;
        } else {
            askPrice.textContent = 'Err';
            bidPrice.textContent = 'Err';
        }
    } catch (e) {
        askPrice.textContent = 'Err';
        bidPrice.textContent = 'Err';
    }
}
