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
        user_icon: string,
        user_steamid: string,
        game_data: {
            playtime_forever: number
        }
    }[]
}
// string[]leaderboard data summaries
type UserGames = {
    appid: number,
    game_title: string,
    game_icon_hash: string,
}[]

async function getFriends() {
    const friends = await fetch(`/api/friends/`)
    return await friends.json()

}

async function getLeaderboard(game_id: number = 730): Promise<GameLeaderboard> {
    const game = await fetch(`/api/leaderboard/${game_id}`)
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
    leaderboard.sort((a, b) => (b.game_data.playtime_forever - a.game_data.playtime_forever) )
    const table = document.getElementById('leaderboard')
    table!.innerHTML = ''
    for (const [i, data] of leaderboard.entries()) {
        const rank = i + 1
        console.log(i, data)

        let rowStyle = {
            bg: '',
            border: 'border-1 border-slate-600',
            text: 'text-slate-600',
            shadow: '',
            svg: ``
        }

        if (rank === 1) {
            rowStyle = {
                bg: 'bg-yellow-500',
                border: '',
                text: 'text-yellow-900',
                shadow: 'shadow-[0_0_20px_rgba(234,179,8,0.3)]',
                svg: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-crown-icon lucide-crown"><path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/></svg>`
            }
        } else if (rank === 2) {
            rowStyle = {
                bg: 'bg-slate-300',
                border: '',
                text: 'text-slate-900',
                shadow: 'shadow-[0_0_20px_rgba(203,213,225,0.2)]',
                svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-medal-icon lucide-medal"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>`
            }
        } else if (rank === 3) {
            rowStyle = {
                bg: 'bg-orange-600',
                border: '',
                text: 'text-white',
                shadow: 'shadow-[0_0_20px_rgba(234,88,12,0.2)]',
                svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-medal-icon lucide-medal"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>`
            }
        }


        const tableRow = `
           <tr class="group hover:bg-white/[0.02] transition-colors relative ">
            <th class="text-center">
              <div class="relative w-12 h-12 flex items-center justify-center ${rowStyle?.border} ${rowStyle.bg} ${rowStyle.text} rounded-2xl ${rowStyle.shadow} font-black text-xl transition-transform ${i in [0, 1, 2] ? 'group-hover:scale-110 group-hover:rotate-3': ''}  duration-300">
                ${i + 1}
                <div class="absolute -top-1.5 -right-1.5 ${i in [0, 1, 2] ? 'bg-slate-900 p-0.5 border border-slate-700': ''} rounded-full  text-white">
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
        const image = document.createElement('img')
        gameBtn.textContent = game.game_title
        gameBtn.className = 'group relative flex items-center gap-4 bg-slate-800/40 hover:bg-slate-800 border border-slate-700/50 hover:border-blue-500/50 p-4 rounded-2xl transition-all hover:shadow-xl hover:-translate-y-1 overflow-hidden'
        // image.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${game.appid}/${game.game_icon_hash}.jpg`
        // gameBtn.appendChild(image)
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

    button.addEventListener('click', async () => {
        selectedGames = button
        await gameClickHandler(game)
        console.log(selectedGames)
    })

    const gamesTitle = document.getElementById('gameTitle')
    gamesTitle!.textContent = `Мои игры (${gamesContainer!.childElementCount})`
}

const gamesContainer = document.getElementById('gameContent')

gameListArea()
addFriends()
addFirstGame()
let selectedGames: HTMLButtonElement

async function gameClickHandler(game: UserGames[0]){
    const title = document.getElementById('title')
    const mainContent = document.getElementById('mainContent')
    const loadingContainer = document.getElementById('loadingContainer')
    const body = document.body
    mainContent!.classList.add('blur-md', 'brightness-15')
    body.classList.add('pointer-events-none', 'overflow-clip')

    const loadingHTML = `
      <div class="absolute top-1/2  left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-1 flex flex-col items-center justify-center" id="loading">
        <div class="w-16 h-16 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin shadow-[0_0_20px_rgba(59,130,246,0.5)]"></div>
        <p class="mt-4 text-blue-400 font-black text-xs uppercase animate-pulse">Загрузка
          данных...
        </p>
      </div>
    `
    const test = `
        <div class="absolute left-1/2 z-52 size-100 bg-lime-500"></div>
    `
    loadingContainer!.classList.add('max-h-screen')
    loadingContainer!.insertAdjacentHTML('afterbegin', loadingHTML)

    const leaderboard = await getLeaderboard(game.appid)
    title!.textContent = leaderboard.game_info.game_title
    await renderLeaderboard(leaderboard.leaderboard)

    document.getElementById('loading')!.remove()
    loadingContainer!.classList.remove('max-h-screen')
    mainContent!.classList.remove('blur-md', 'brightness-15')
    body.classList.remove('pointer-events-none', 'overflow-clip')
}