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
    return __awaiter(this, void 0, void 0, function* () {
        const game = yield fetch('/api/leaderboard/730');
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
            p.className = ('text-[12px] font-semibold group-hover:text-slate-400');
            img.className = ('size-6 rounded-full');
            button.className = ('flex items-center mb-2 gap-x-2 text-white group hover:bg-slate-800');
            button.appendChild(img);
            button.appendChild(p);
            friendsContainer.appendChild(button);
        }
        const friendsTitle = document.getElementById('friendTitle');
        friendsTitle.textContent = `Список друзей (${friends.length})`;
    });
}
function renderLeaderboard(leaderboard) {
    return __awaiter(this, void 0, void 0, function* () {
        const table = document.getElementById('leaderboard');
        for (const [i, data] of leaderboard.entries()) {
            console.log(i, data);
            const tableRow = `
           <tr>
            <th>${i + 1}</th>
            <td>${data.user_name}</td>
            <td>${data.game_data.playtime_forever}</td>
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
        const gameLeaderboard = yield getLeaderboard();
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
        const userGames = yield getUserGames();
        for (const game of userGames) {
            const gameBtn = document.createElement('button');
            gameBtn.textContent = game.game_title;
            gameBtn.className = 'group relative flex items-center gap-4 bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-blue-500/50 p-4 rounded-2xl transition-all hover:shadow-xl hover:-translate-y-1 overflow-hidden';
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
        selectedGames = button;
        p.textContent = game.game_title;
        img.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${game.appid}/${game.game_icon_hash}.jpg`;
        p.className = ('text-[12px] font-semibold group-hover:text-slate-400');
        img.className = ('size-6 rounded-full');
        button.className = ('flex items-center mb-2 gap-x-2 text-white group hover:bg-slate-800');
        button.appendChild(img);
        button.appendChild(p);
        gamesContainer.appendChild(button);
        button.addEventListener('click', () => {
            selectedGames = button;
            console.log(selectedGames);
        });
        const gamesTitle = document.getElementById('gameTitle');
        gamesTitle.textContent = `Мои игры (${gamesContainer.childElementCount})`;
    });
}
const gamesContainer = document.getElementById('gameContent');
gameListArea();
// addFriends()
// addFirstGame()
let selectedGames;
// addFriends()
// addFirstGame()
