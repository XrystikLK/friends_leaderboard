"use strict";
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
            const div = document.createElement('div');
            const img = document.createElement('img');
            const p = document.createElement('p');
            p.textContent = friend.personaname;
            img.src = friend.avatar_url;
            p.className = ('text-[16px] font-semibold');
            img.className = ('size-10 rounded-full');
            div.className = ('flex items-center mb-2 gap-x-2');
            div.appendChild(img);
            div.appendChild(p);
            friendsContainer.appendChild(div);
        }
        const friendsTitle = document.getElementById('friendTitle');
        friendsTitle.textContent = `Список друзей (${friends.length})`;
    });
}
addFriends();
