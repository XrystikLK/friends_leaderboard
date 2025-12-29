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
function addFirstGame() {
    return __awaiter(this, void 0, void 0, function* () {
        const game = yield fetch('/api/leaderboard/730');
        const gameLeaderboard = yield game.json();
        const gamesContainer = document.getElementById('gameContent');
        const button = document.createElement('button');
        const img = document.createElement('img');
        const p = document.createElement('p');
        p.textContent = gameLeaderboard.game_info.game_title;
        img.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${gameLeaderboard.game_info.appid}/${gameLeaderboard.game_info.game_icon_hash}.jpg`;
        p.className = ('text-[12px] font-semibold group-hover:text-slate-400');
        img.className = ('size-6 rounded-full');
        button.className = ('flex items-center mb-2 gap-x-2 text-white group hover:bg-slate-800');
        button.appendChild(img);
        button.appendChild(p);
        gamesContainer.appendChild(button);
        const gamesTitle = document.getElementById('gameTitle');
        console.log(gamesTitle);
        gamesTitle.textContent += ` (${1})`;
    });
}
addFriends();
addFirstGame();
// fetch('/api/leaderboard/730')
