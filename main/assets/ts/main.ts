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
        }[]
    }
}

async function getFriends() {
    const friends = await fetch(`/api/friends/`)
    return await friends.json()

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

async function addFirstGame() {
    const game = await fetch('/api/leaderboard/730')
    const gameLeaderboard: GameLeaderboard = await game.json()
    const gamesContainer = document.getElementById('gameContent')

    const button = document.createElement('button')
    const img = document.createElement('img')
    const p = document.createElement('p')
    p.textContent = gameLeaderboard.game_info.game_title
    img.src = `http://media.steampowered.com/steamcommunity/public/images/apps/${gameLeaderboard.game_info.appid}/${gameLeaderboard.game_info.game_icon_hash}.jpg`
    p.className = ('text-[12px] font-semibold group-hover:text-slate-400')
    img.className = ('size-6 rounded-full')
    button.className = ('flex items-center mb-2 gap-x-2 text-white group hover:bg-slate-800')
    button.appendChild(img)
    button.appendChild(p)
    gamesContainer!.appendChild(button)

    const gamesTitle = document.getElementById('gameTitle')
    console.log(gamesTitle)
    gamesTitle!.textContent +=  ` (${1})`
}

addFriends()
addFirstGame()
// fetch('/api/leaderboard/730')


