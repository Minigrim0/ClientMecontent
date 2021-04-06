const Command = require('./command');
const {Client} = require('pg');

// clients will also use environment variables
// for connection information
const pg_client = new Client()
pg_client.connect()

async function query(){
    await pg_client.connect()
    res = await pg_client.query(queryCheckUser, [message.member.user.id])
}

module.exports = class AddWord extends Command{
	static match(message){
		if(message.content.startsWith('!addword')){
			return true
		}
		return false
	}
	
	static action(message){
        message.delete()
		if(message.member.displayColor === 15277667){
			var args = message.content.split(' ')

            var queryCheckUser = "SELECT id from users WHERE username=$1";
            var user_registered = false;
            var userID = null;
            var res = null;

            try {
                res = await pg_client.query(queryCheckUser, [message.member.user.id])
            }
            catch (err) {
                 console.log(err.stack)
            }
            if(res['rows'][0] != null){
                user_registered = true;
                userID = res['rows'][0]['id'];
            }

            // To associate the ID with the user
            //console.log("user = " + message.channel.members.get(message.member.user.id).displayName);

            if (!user_registered){
                var queryAddUser = "INSERT INTO users (username) VALUES ($1)";
                try{
                    (async() => {
                        res = await pg_client.query(queryAddUser, [message.member.user.id])
                    })();
                }
                catch (err){
                    console.log("Error : " + err.stack)
                }
                try{
                    (async() => {
                        res = await pg_client.query(queryCheckUser, [message.member.user.id]);
                    })();
                }
                catch(err){
                    console.log("Error : " + err.stack);
                }
                if(res['rows'][0] != null){
                    userID = res['rows'][0]['id'];
                }
            }
            pg_client.query(
                'INSERT INTO PROPOSITIONS (content, user_id) VALUES (\'' + args[1] + '\', \'' + userID + '\')',
                (err, res) => {if(err) console.log("Error : " + err)}
            )
			message.channel.send('\'' + args[1] + '\' ajouté à l\'index')
		}else{
			message.channel.send('Vous n\'avez pas les droits pour ajouter des mots !')
		}
	}
}
