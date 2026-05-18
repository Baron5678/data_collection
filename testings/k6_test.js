import http from 'k6/http';

export const options = {
    vus: 50,
    duration: '30s',
};

export default function () {
    const payload = {
        username: 'Igor',
        phone: '123456789',
    };

    const params = {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    };

    http.post(
        'http://89.168.106.107/users_sync',
        payload,
        params
    );
}