const Discord = require('discord.js')

const bot = new Discord.Client()
const startbot = require('./commands/StartBot')
const addword  = require('./commands/addWord')
const unknown  = require('./commands/Unknown')

bot.on('ready', function(){
	bot.user.setActivity('emmerder son monde').catch(console.error)
})

bot.on('message', function(msg){
	let commandUsed = 
		startbot.parse(msg) ||
		addword.parse(msg) ||
		unknown.parse(msg)
}	
)

var key = process.env.API_KEY;
bot.login(key);
