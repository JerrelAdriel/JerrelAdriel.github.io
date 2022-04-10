const karakter = document.getElementById('karakter')
const rintangan = document.getElementById('rintangan')
const startgame = document.getElementById('startgame')
const startagain = document.getElementById('start')
const sound = document.getElementById('sound')


const lari = () => {
    sound.play()
    karakter.classList.add('animasiLompat')
    rintangan.classList.add('animasiRintangan')
    startgame.classList.remove('startgame')
    startagain.classList.remove('play-again')
    setTimeout(function removeJump(){
        karakter.classList.remove('animasiLompat')
    }, 300)
}


const gameOver = () => {
    const karakterTop = parseInt(window.getComputedStyle(karakter).getPropertyValue('top'))
    const rintanganLeft = parseInt(window.getComputedStyle(rintangan).getPropertyValue('left'))
    if(rintanganLeft > 50 && rintanganLeft < 70 && karakterTop > 120){
        alert('Game Over')
        rintangan.classList.remove('animasiRintangan')
        karakter.classList.remove('animasiLompat')
        startagain.classList.add('play-again')
        
    }

}
startgame.classList.add('startgame')
document.addEventListener('click',lari)
setInterval(gameOver, 10)
