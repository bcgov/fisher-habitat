let api_base_url = ''
let tile_server_fisher = ''
if(window.location.origin == 'http://localhost:8080'){
    api_base_url='http://localhost:8000/api'
    tile_server_fisher = 'http://localhost:7800'
} else {
    api_base_url= window.location.origin + '/api'
    tile_server_fisher = window.location.origin + '/tiles'
}

export const API_BASE_URL = api_base_url
export const TILE_SERVER_FISHER = tile_server_fisher