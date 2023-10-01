import request from '@/utils/request'

// profile api
export function getProfile(params) {
  return request({
    url: '/api/profile/',
    method: 'get',
    params,
  })
}
export function getProfileDetail(params) {
  return request({
    url: '/api/profile/' + params.id + '/',
    method: 'get',
    params,
  })
}

export function patchProfile(data, id) {
  return request({
    url: '/api/profile/' + id + '/',
    method: 'patch',
    data,
  })
}

export function getProfileChangeAvatar(params, id) {
  return request({
    url: '/api/profile/' + id + '/change_avatar/',
    method: 'get',
    params,
  })
}

export function changeFaceAlbumName(data) {
  return request({
    url: '/api/profile/' + data.id + '/',
    method: 'put',
    data,
  })
}

export function clear_face_album(params) {
  return request({
    url: '/api/profile/clear_face_album/',
    method: 'get',
  })
}

export function getFilterList(params) {
  return request({
    url: '/api/profile/get_filtered_list/',
    method: 'get',
    params,
  })
}
