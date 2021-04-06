const { Client } = require('pg')
const pgClient = new Client()

;(async () => {
  await pgClient.connect()
  const res = await pgClient.query('SELECT $1::text as message', ['Hello world!'])
  console.log(res.rows[0].message) // Hello world!
  await pgClient.end()
})()
