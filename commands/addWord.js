const Command = require('./command')
var fs = require("fs")

module.exports = class AddWord extends Command{
	static match(message){
		if(message.content.startsWith('!addword')){
			return true
		}
		return false
	}
	
	static action(message){
		if(message.member.displayColor === 15277667){
			var args = message.content.split(' ')
			var newWord = ","
			for(var i=1;i<args.length;i++){
				newWord += args[i] + ' '
			}
			var content = fs.readFileSync('./WordIndex.txt', "UTF-8")
			fs.writeFileSync("./WordIndex.txt", content + newWord, "UTF-8");
			message.channel.send('\'' + newWord + '\' ajouté à l\'index')
			message.delete()
		}else{
			message.channel.send('Vous n\'avez pas les droits pour ajouter des mots !')
			message.delete()
		}
	}
}