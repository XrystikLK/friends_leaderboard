async function getFriends(){
    const friends = await fetch(`/api/friends/`)
    return await friends.json()

}
async function addFriends(){
    const friendsContainer = document.getElementById('friendContent')
    const friends = await getFriends()
    for (let friend of friends){
        const div = document.createElement('div')
        const img = document.createElement('img')
        const p = document.createElement('p')
        p.textContent = friend.personaname
        img.src = friend.avatar_url
        p.className = ('text-[16px] font-semibold')
        img.className = ('size-10 rounded-full')
        div.className = ('flex items-center mb-2 gap-x-2')
        div.appendChild(img)
        div.appendChild(p)
        friendsContainer!.appendChild(div)
    }
    const friendsTitle = document.getElementById('friendTitle')
    friendsTitle!.textContent = `Список друзей (${friends.length})`
}
addFriends()


