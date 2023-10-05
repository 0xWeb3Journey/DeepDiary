import request from '@/utils/request'

// demand api
export function getDemand(params) {
  return request({
    url: '/api/demand/',
    method: 'get',
    params,
  })
}

export function addDemand(data) {
  return request({
    url: '/api/demand/',
    method: 'post',
    data,
  })
}

export function changeDemand(params, id) {
  return request({
    url: '/api/demand/' + id + '/',
    method: 'put',
    data: params,
  })
}
