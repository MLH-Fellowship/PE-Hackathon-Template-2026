import http from 'k6/http';
import { check, sleep } from 'k6';

// Test configuration: 50 concurrent users for 1 minute
export const options = {
  vus: 50,        // 50 concurrent virtual users
  duration: '1m', // run for 1 minute
};

// Sample short codes from the seed data (urls.csv)
const shortCodes = [
  '0Y7puX', 'joOewJ', 'YMwcJp', 'gHOkuS', 'aPgkMG',
  'IKhHtb', '6mStl9', 'wx48gY', '1U9mdL', 'Uk5jxw',
  'jHH6Rw', 'yQSwT2', 'ULUAiE', '3mgDRW', 'xwMpkA',
  'VgkwPM', 'H8r4XJ', 'afSvrh', 'ANQfSc'
];

const BASE_URL = 'http://localhost:5000';

export default function () {
  // Pick a random short code from the list
  const shortCode = shortCodes[Math.floor(Math.random() * shortCodes.length)];
  
  // Test the URL redirect endpoint (core functionality)
  const response = http.get(`${BASE_URL}/${shortCode}`, {
    redirects: 0, // Don't follow redirects, just check the response
  });
  
  // Verify the response
  check(response, {
    'redirect or not found': (r) => r.status === 302 || r.status === 404,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  // Add think time between requests (1 second)
  sleep(1);
}
