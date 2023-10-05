import request from '@/utils/request'

// resource api
export function getResource(params) {
  return request({
    url: '/api/resource/',
    method: 'get',
    params,
  })
}

export function addResource(data) {
  return request({
    url: '/api/resource/',
    method: 'post',
    data,
  })
}

export function changeResource(params, id) {
  return request({
    url: '/api/resource/' + id + '/',
    method: 'put',
    data: params,
  })
}
