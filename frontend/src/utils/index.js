import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt){
    if (!jwt || jwt.split('.').length < 3){
        return false
    }
    const data = JSON.parse(atob(jwt.split('.')[1]))
    const exp = new Date(data.exp * 1000)
    const now = new Date()
    console.log(( exp - now ) / 60)
    console.log('IS_VALID_JWT FUNC RESULT:')
    console.log(now<exp)
    return now < exp
}