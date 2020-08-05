const Command = require('./command')
var fs = require("fs")

//WordArray contient les mots susceptibles d'etre tirés au hasard
var WordsArray = []
var content = fs.readFileSync('./WordIndex.txt', "UTF-8")

WordsArray = content.split(',')

module.exports = class StartBot extends Command{
	static match(message){
		if(message.channel.name === 'le-client-mécontent'){
			if(message.content.startsWith('!')){
				return message.content.startsWith('!startgame') || message.content.startsWith('!reload') || message.content.startsWith('!showlist')
			}else{
				if(message.member.user.username != 'Client Mécontent'){
					console.log('Deleting -> ' + message.content + ' - From : ' + message.member.id)
					message.delete()
				}
				return false
			}
		}
		if(message.content.startsWith('!startgame')){
			message.delete()
			message.channel.send('Eh gros con de @' + message.member.user.username + ', si tu veux faire cette commande, c\'est moi qu\'il faut venir voir, là t\'es sur le mauvais chat !')
		}
		return false
	}

	static action(message){
		if(message.content.startsWith('!startgame')){

			message.delete()

			var firstWord = Math.round(Math.random() * WordsArray.length)
			var secondWord = Math.round(Math.random() * WordsArray.length)
			while(secondWord === firstWord){
                secondWord = Math.round(Math.random() * WordsArray.length)
            }
			var thirdWord = Math.round(Math.random() * WordsArray.length)
			while(thirdWord === firstWord || thirdWord === secondWord){
                thirdWord = Math.round(Math.random() * WordsArray.length)
            }

			console.log(firstWord)
			console.log(secondWord)
			console.log(thirdWord)

			message.channel.send(
			'----( DÉFI )---- \n'
			+ 'Je veux une photo qui contient...' + ' **'
			+ WordsArray[firstWord] + '**, **'
			+ WordsArray[secondWord] + '** Et **'
			+ WordsArray[thirdWord] + '** ! '
			+ 'Bonne merde photographes en herbe !')
		}
		if(message.content.startsWith('!reload')){
			content = fs.readFileSync('./WordIndex.txt', "UTF-8")
			WordsArray = content.split(',')
			message.channel.send('JE SUIS A JOUR !')
			message.delete()
		}
		if(message.content.startsWith('!showlist')){
			var msg = ""
			for(var i=0;i<WordsArray.length;i++){
				msg += WordsArray[i] + ', '
			}
			message.channel.send(msg)
			message.delete()
		}
	}
}
