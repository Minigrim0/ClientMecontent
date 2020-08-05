const Command = require('./command')

module.exports = class StartBot extends Command{
	static match(message){
		if(message.channel.name === 'le-client-mécontent'){
			if(message.content.startsWith('!')){
				return true
			}
			return false
		}
		return false
	}
	
	static action(message){
		if(message.member.user.username != 'Client Mécontent'){
			message.delete()
			return message.channel.send('Commande \'' + message.content + '\' inconnue, message supprimé')
		}
	}
}