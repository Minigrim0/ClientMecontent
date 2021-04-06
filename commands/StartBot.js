const Command = require('./command');
const {Client} = require('pg');

// clients will also use environment variables
// for connection information
const pg_client = new Client();

module.exports = class StartBot extends Command{
	static match(message){
		if(message.channel.name === 'le-client-mécontent'){
			if(message.content.startsWith('!')){
				return message.content.startsWith('!startgame') || message.content.startsWith('!showlist')
			}else{
				if(message.member.user.username != 'Client Mécontent'){
					console.log('Deleting -> ' + message.content + ' - From : ' + message.member.id)
					message.delete()
				}
				return false
			}
		}
		else if(message.content.startsWith('!startgame') || message.content.startsWith('!showlist')){
			message.delete()
			message.channel.send('Eh gros con de @' + message.member.user.username + ', si tu veux faire cette commande, c\'est moi qu\'il faut venir voir, là t\'es sur le mauvais chat !')
		}
		return false
	}

	static action(message){
        pg_client.connect();
        message.delete();

        if(message.content.startsWith('!startgame')){
            var nb_props = 150;
            pg_client.query(
                'SELECT COUNT(*) FROM PROPOSITIONS',
                (err, res) => {
                    nb_props = res['rows'][0]['count']
                }
            )

            if(nb_props < 3){
			    pg_client.end();
                message.channel.send("Il n'y a pas assez de mots dans la base de donnée pour lancer une partie !")
                return
            }

			var firstWord = Math.round(Math.random() * nb_props)
			var secondWord = Math.round(Math.random() * nb_props)
			while(secondWord === firstWord){
                secondWord = Math.round(Math.random() * nb_props)
            }
			var thirdWord = Math.round(Math.random() * nb_props)
			while(thirdWord === firstWord || thirdWord === secondWord){
                thirdWord = Math.round(Math.random() * nb_props)
            }

			message.channel.send(
                '----( DÉFI )---- \n'
                + 'Je veux une photo qui contient...' + ' **'
                + "chausette" + '**, **'
                + "bite" + '** Et **'
                + "chausette" + '** ! '
                + 'Bonne merde photographes en herbe !');
		}
		else if(message.content.startsWith('!showlist')){
			var msg = ""
			for(var i=0;i<WordsArray.length;i++){
				msg += WordsArray[i] + ', '
			}
			message.channel.send(msg)
		}
        pg_client.end();
	}
}
