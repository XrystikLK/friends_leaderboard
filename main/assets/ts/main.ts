// type GameLeaderboard = {
//     user_name: string,
//     game_data: {
//         game_id: number,
//         playtime_forever: number
//     }
// }[]

type GameLeaderboard = {
    game_info: {
        appid: number,
        game_icon_hash: string,
        game_title: string
    }
    leaderboard: {
        user_name: string,
        game_data: {
            playtime_forever: number
        }
    }[]
}
// string[]
type UserGames = {
    appid: number,
    game_title: string,
    game_icon_hash: string,
}[]

async function getFriends() {
    const friends = await fetch(`/api/friends/`)
    return await friends.json()

}

async function getLeaderboard() {
    const game = await fetch('/api/leaderboard/730')
    return await game.json()
}

async function getUserGames() {
    let games = await fetch('/api/games/')
    return await games.json()
}

async function addFriends() {
    const friendsContainer = document.getElementById('friendContent')
    const friends = await getFriends()
    for (let friend of friends) {
        const button = document.createElement('button')
        const img = document.createElement('img')
        const p = document.createElement('p')
        p.textContent = friend.personaname
        img.src = friend.avatar_url
        p.className = ('text-[12px] font-semibold group-hover:text-slate-400')
        img.className = ('size-6 rounded-full')
        button.className = ('flex items-center mb-2 gap-x-2 text-white group hover:bg-slate-800')
        button.appendChild(img)
        button.appendChild(p)
        friendsContainer!.appendChild(button)
    }
    const friendsTitle = document.getElementById('friendTitle')
    friendsTitle!.textContent = `Список друзей (${friends.length})`
}

async function renderLeaderboard(leaderboard: GameLeaderboard['leaderboard']) {
    const table = document.getElementById('leaderboard')
    for (const [i, data] of leaderboard.entries()) {
        console.log(i, data)
        const tableRow = `
           <tr>
            <th>${i + 1}</th>
            <td>${data.user_name}</td>
            <td>${data.game_data.playtime_forever}</td>
            <td></td>
          </tr>
        `
        table!.insertAdjacentHTML('beforeend', tableRow)
    }


    // $0.insertAdjacentHTML('beforeend', newRow);
    // leaderboard
}

async function addFirstGame() {
    const gameLeaderboard: GameLeaderboard = await getLeaderboard()
    await addGameToList(gameLeaderboard.game_info)
    await renderLeaderboard(gameLeaderboard.leaderboard)
}

async function gameListArea() {
    const addGameBtn = document.getElementById('addGame')
    const addGameArea = document.getElementById('addGameArea')
    const gamesList = document.getElementById('gamesList')

    addGameBtn!.addEventListener('click', () => {
        if (addGameArea!.classList.contains('hidden')) {
            addGameArea!.classList.remove('hidden')
        } else {
            addGameArea!.classList.add('hidden')
        }
    })

    const userGames: UserGames = await getUserGames()
    for (const game of userGames) {
        const gameBtn = document.createElement('button')
        gameBtn.textContent = game.game_title
        gameBtn.className = 'group relative flex items-center gap-4 bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-blue-500/50 p-4 rounded-2xl transition-all hover:shadow-xl hover:-translate-y-1 overflow-hidden'
        gameBtn.onclick = async () => {
            await addGameToList(game)
            gameBtn.remove()
        }
        gamesList!.appendChild(gameBtn)
    }

}

async function addGameToList(game: UserGames[0]) {
    const button = document.createElement('button')
    const img = document.createElement('img')
    const p = document.createElement('p')
    selectedGames = button
    p.textContent = game.game_title
    img.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${game.appid}/${game.game_icon_hash}.jpg`
    p.className = ('text-[12px] font-semibold group-hover:text-slate-400')
    img.className = ('size-6 rounded-full')
    button.className = ('flex items-center mb-2 gap-x-2 text-white group hover:bg-slate-800')
    button.appendChild(img)
    button.appendChild(p)
    gamesContainer!.appendChild(button)

    button.addEventListener('click', () => {
        selectedGames = button
        console.log(selectedGames)
    })

    const gamesTitle = document.getElementById('gameTitle')
    gamesTitle!.textContent = `Мои игры (${gamesContainer!.childElementCount})`
}

const gamesContainer = document.getElementById('gameContent')

gameListArea()
// addFriends()
// addFirstGame()
let selectedGames: HTMLButtonElement
// addFriends()
// addFirstGame()


