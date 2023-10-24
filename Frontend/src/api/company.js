import request from '@/utils/request'

// Company api
export function getCompany(params) {
  return request({
    url: '/api/company/',
    method: 'get',
    params,
  })
}
export function getCompanyDetail(params) {
  return request({
    url: '/api/company/' + params.id + '/',
    method: 'get',
    params,
  })
}

export function patchCompany(data, id) {
  return request({
    url: '/api/company/' + id + '/',
    method: 'patch',
    data,
  })
}

export function getCompanyChangeAvatar(params, id) {
  return request({
    url: '/api/company/' + id + '/change_avatar/',
    method: 'get',
    params,
  })
}

export function changeFaceAlbumName(data) {
  return request({
    url: '/api/company/' + data.id + '/',
    method: 'put',
    data,
  })
}

export function clear_face_album(params) {
  return request({
    url: '/api/company/clear_face_album/',
    method: 'get',
  })
}

export function getFilterList(params) {
  return request({
    url: '/api/company/get_filtered_list/',
    method: 'get',
    params,
  })
}
