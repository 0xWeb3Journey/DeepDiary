import request from '@/utils/request'

// face api
export function getFace(params) {
  return request({
    url: '/api/face/',
    method: 'get',
    params,
  })
}

export function changeFaceName(params) {
  return request({
    url: '/api/face/' + params.id + '/',
    method: 'put',
    data: params,
  })
}

export function getFilterList(params) {
  console.log(params)
  return request({
    url: '/api/face/get_filtered_list/',
    method: 'get',
    params,
  })
}
