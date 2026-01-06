"use strict";
// type GameLeaderboard = {
//     user_name: string,
//     game_data: {
//         game_id: number,
//         playtime_forever: number
//     }
// }[]
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function getFriends() {
    return __awaiter(this, void 0, void 0, function* () {
        const friends = yield fetch(`/api/friends/`);
        return yield friends.json();
    });
}
function getLeaderboard() {
    return __awaiter(this, arguments, void 0, function* (game_id = 730) {
        const game = yield fetch(`/api/leaderboard/${game_id}`);
        return yield game.json();
    });
}
function getUserGames() {
    return __awaiter(this, void 0, void 0, function* () {
        let games = yield fetch('/api/games/');
        return yield games.json();
    });
}
function addFriends() {
    return __awaiter(this, void 0, void 0, function* () {
        const friendsContainer = document.getElementById('friendContent');
        const friends = yield getFriends();
        for (let friend of friends) {
            const button = document.createElement('button');
            const img = document.createElement('img');
            const p = document.createElement('p');
            p.textContent = friend.personaname;
            img.src = friend.avatar_url;
            p.className = ('text-[14px] font-semibold group-hover:text-slate-400 text-justify');
            img.className = ('size-9 rounded-full');
            button.className = ('w-full flex items-center gap-x-2 text-white group hover:bg-slate-800 py-2 px-2 rounded-[12px]');
            button.appendChild(img);
            button.appendChild(p);
            friendsContainer.appendChild(button);
        }
        const friendsTitle = document.getElementById('friendTitle');
        friendsTitle.textContent = `СПИСОК ДРУЗЕЙ (${friends.length})`;
    });
}
function renderLeaderboard(leaderboard) {
    return __awaiter(this, void 0, void 0, function* () {
        leaderboard.sort((a, b) => (b.game_data.playtime_forever - a.game_data.playtime_forever));
        const table = document.getElementById('leaderboard');
        table.innerHTML = '';
        for (const [i, data] of leaderboard.entries()) {
            const rank = i + 1;
            console.log(i, data);
            let rowStyle = {
                bg: '',
                border: 'border-1 border-slate-600',
                text: 'text-slate-600',
                shadow: '',
                svg: ``
            };
            if (rank === 1) {
                rowStyle = {
                    bg: 'bg-yellow-500',
                    border: '',
                    text: 'text-yellow-900',
                    shadow: 'shadow-[0_0_20px_rgba(234,179,8,0.3)]',
                    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-crown-icon lucide-crown"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>`
                };
            }
            else if (rank === 2) {
                rowStyle = {
                    bg: 'bg-slate-300',
                    border: '',
                    text: 'text-slate-900',
                    shadow: 'shadow-[0_0_20px_rgba(203,213,225,0.2)]',
                    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-medal-icon lucide-medal"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>`
                };
            }
            else if (rank === 3) {
                rowStyle = {
                    bg: 'bg-orange-600',
                    border: '',
                    text: 'text-white',
                    shadow: 'shadow-[0_0_20px_rgba(234,88,12,0.2)]',
                    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-medal-icon lucide-medal"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>`
                };
            }
            const tableRow = `
           <tr class="group hover:bg-white/[0.02] transition-colors relative ">
            <th class="flex justify-center">
              <div class="relative w-12 h-12 flex items-center justify-center ${rowStyle === null || rowStyle === void 0 ? void 0 : rowStyle.border} ${rowStyle.bg} ${rowStyle.text} rounded-2xl ${rowStyle.shadow} font-black text-xl transition-transform ${i in [0, 1, 2] ? 'group-hover:scale-110 group-hover:rotate-3' : ''}  duration-300">
                ${i + 1}
                <div class="absolute -top-1.5 -right-1.5 ${i in [0, 1, 2] ? 'bg-slate-900 p-0.5 border border-slate-700' : ''} rounded-full  text-white">
                  ${rowStyle.svg}
                </div>
              </div>
            </th>
            <td>
              <div class="flex items-center space-x-2">
                <img src='${data.user_icon}' class="size-13 rounded-[8px] group-hover:scale-110 transition-all"/>
                <div class="">
                  <p class="font-bold text-[18px]">${data.user_name}</p>
                  <p class="text-slate-500 text-[10px] font-semibold">STEAM ID:${data.user_steamid}</p>
                </div>
              </div>
            </td>
            <td>${data.game_data.playtime_forever} Ч.</td>
            <td></td>
          </tr>
        `;
            table.insertAdjacentHTML('beforeend', tableRow);
        }
        // $0.insertAdjacentHTML('beforeend', newRow);
        // leaderboard
    });
}
function addFirstGame() {
    return __awaiter(this, void 0, void 0, function* () {
        yield addGameToList(gameLeaderboard.game_info);
        yield renderLeaderboard(gameLeaderboard.leaderboard);
    });
}
function gameListArea() {
    return __awaiter(this, void 0, void 0, function* () {
        const addGameBtn = document.getElementById('addGame');
        const addGameArea = document.getElementById('addGameArea');
        const gamesList = document.getElementById('gamesList');
        addGameBtn.addEventListener('click', () => {
            if (addGameArea.classList.contains('hidden')) {
                addGameArea.classList.remove('hidden');
            }
            else {
                addGameArea.classList.add('hidden');
            }
        });
        for (const game of userGames) {
            const gameBtn = document.createElement('button');
            const image = document.createElement('img');
            gameBtn.innerHTML = `
            <div class="group relative flex items-center gap-4 bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-blue-500/50 p-4 rounded-2xl transition-all hover:shadow-xl hover:-translate-y-1 overflow-hidden">
              <img src="https://cdn.akamai.steamstatic.com/steam/apps/${game.appid}/header.jpg" class="size-14 rounded-[12px] object-cover"/>
              <div class="flex flex-col text-start">
                <p class="text-sm font-black text-slate-100 group-hover:text-blue-400 transition-colors line-clamp-2">${game.game_title}</p>
                <p class="text-[10px] text-slate-500 mt-1 font-bold uppercase group-hover:text-slate-300 transition-colors">appid: ${game.appid}</p>
              </div>
            </div>
        `;
            // gameBtn.textContent = game.game_title
            // gameBtn.className = 'group relative flex items-center gap-4 bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-blue-500/50 p-4 rounded-2xl transition-all hover:shadow-xl hover:-translate-y-1 overflow-hidden'
            // image.src = `https://cdn.akamai.steamstatic.com/steam/apps/${game.appid}/header.jpg`
            // image.classList.add('size-14', 'rounded-[12px]', 'object-cover')
            // gameBtn.appendChild(image)
            gameBtn.onclick = () => __awaiter(this, void 0, void 0, function* () {
                yield addGameToList(game);
                gameBtn.remove();
            });
            gamesList.appendChild(gameBtn);
        }
    });
}
function addGameToList(game) {
    return __awaiter(this, void 0, void 0, function* () {
        const button = document.createElement('button');
        const img = document.createElement('img');
        const p = document.createElement('p');
        selectedGame = button;
        p.textContent = game.game_title;
        img.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${game.appid}/${game.game_icon_hash}.jpg`;
        p.className = ('text-[14px] font-semibold group-hover:text-slate-400 text-justify');
        img.className = ('size-9 rounded-full');
        button.className = ('w-full flex items-center gap-x-2 text-white group hover:bg-slate-800 py-2 px-2 rounded-[12px]');
        button.appendChild(img);
        button.appendChild(p);
        gamesListContainer.appendChild(button);
        button.addEventListener('click', () => __awaiter(this, void 0, void 0, function* () {
            selectedGame = button;
            yield gameClickHandler(game);
            console.log(selectedGame);
        }));
        const gamesTitle = document.getElementById('gameTitle');
        gamesTitle.textContent = `МОИ ИГРЫ (${gamesListContainer.childElementCount})`;
    });
}
function gameClickHandler(game) {
    return __awaiter(this, void 0, void 0, function* () {
        const title = document.getElementById('title');
        const mainContent = document.getElementById('mainContent');
        const loadingContainer = document.getElementById('loadingContainer');
        const body = document.body;
        mainContent.classList.add('blur-md', 'brightness-15');
        body.classList.add('pointer-events-none', 'overflow-clip');
        const loadingHTML = `
      <div class="absolute top-1/2  left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-1 flex flex-col items-center justify-center" id="loading">
        <div class="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin shadow-[0_0_20px_rgba(59,130,246,0.5)]"></div>
        <p class="mt-4 text-blue-400 font-black text-xs uppercase animate-pulse">Загрузка
          данных...
        </p>
      </div>
    `;
        const test = `
        <div class="absolute left-1/2 z-52 size-100 bg-lime-500"></div>
    `;
        loadingContainer.classList.add('max-h-screen');
        loadingContainer.insertAdjacentHTML('afterbegin', loadingHTML);
        const leaderboard = yield getLeaderboard(game.appid);
        title.textContent = leaderboard.game_info.game_title;
        yield renderTableWidgets(leaderboard.leaderboard);
        yield renderLeaderboard(leaderboard.leaderboard);
        document.getElementById('loading').remove();
        loadingContainer.classList.remove('max-h-screen');
        mainContent.classList.remove('blur-md', 'brightness-15');
        body.classList.remove('pointer-events-none', 'overflow-clip');
    });
}
function renderTableWidgets(leaderboard) {
    return __awaiter(this, void 0, void 0, function* () {
        const time = document.getElementById('timeWidget');
        const users = document.getElementById('usersWidget');
        const leader = document.getElementById('leaderWidget');
        time.textContent = `${(leaderboard.reduce((accumulator, currentValue) => accumulator + currentValue.game_data.playtime_forever, 0)).toLocaleString()} ч.`;
        users.textContent = leaderboard.length.toString();
        leaderboard.sort((a, b) => (b.game_data.playtime_forever - a.game_data.playtime_forever));
        leader.textContent = leaderboard[0].user_name;
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        userGames = yield getUserGames();
        const random_game = userGames[Math.floor(Math.random() * userGames.length)];
        userGames = userGames.filter(game => game.appid !== random_game.appid);
        gameListArea();
        addFriends();
        addGameToList(random_game);
        selectedGame = gamesListContainer.firstElementChild;
        selectedGame.click();
        // addFirstGame()
    });
}
const gamesListContainer = document.getElementById('gameContent');
let selectedGame;
let userGames;
main();
