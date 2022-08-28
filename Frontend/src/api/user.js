import request from '@/utils/request'
import { encryptedData } from '@/utils/encrypt'
import { loginRSA, tokenName } from '@/config'

export async function login(data) {
  if (loginRSA) {
    console.log(data)
    data = await encryptedData(data)
    console.log(data)
  }
  return request({
    url: '/login/',
    method: 'post',
    data,
  })
}

export function getUserInfo(accessToken) {
  return request({
    url: '/api/user/info/',
    method: 'post',
    data: {
      // [tokenName]: accessToken,
      token: accessToken,
      // username: 'blue',
      // password: 'deep-diary666',
    },
  })
}

export function logout() {
  return request({
    url: '/api/user/logout/',
    method: 'post',
  })
}

export function register() {
  return request({
    url: '/register',
    method: 'post',
  })
}
