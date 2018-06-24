import React, { Component } from 'react';
import { View , TouchableOpacity, Modal, TextInput, Image,Text,Button, ToastAndroid, Alert} from 'react-native';
import Expo from 'expo';

export default class FingerprintScan extends Component {
	constructor(){
		super();
		this.state = {response: 'INIT', colorDict: {INIT:'#FAFAFA',NOK:'#e09a9a',OK:'#DCFDC8'},modalVisible: true, uri:''}; // Possible values of response are OK NOK and INIT
	}

  	openModal() {
    	this.setState({modalVisible:true});
  	}

  	closeModal() {
    	this.setState({modalVisible:false});
  	}

	onScan(res) {
		if(res==true){
			fetch(this.state.uri, {
				method: 'POST',
				headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				},
				body: JSON.stringify({
				thumbRight: 'ABCD5',
				}),
			}).then(res=>{this.setState({response:'OK'},()=>setTimeout(()=>{this.setState({response:'INIT'})},3000))}).catch(err=>{ToastAndroid.show('Fingerprinting Server Down',1000);this.setState({response:'NOK'},()=>setTimeout(()=>{this.setState({response:'INIT'})},3000))});
		} else{
			fetch(this.state.uri, {
				method: 'POST',
				headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				},
				body: JSON.stringify({
				XXXX: 'XXXX',
				}),
			}).then(res=>{this.setState({response:'OK'},()=>setTimeout(()=>{this.setState({response:'INIT'})},3000))}).catch(err=>{ToastAndroid.show('Fingerprinting Server Down',1000);this.setState({response:'NOK'},()=>setTimeout(()=>{this.setState({response:'INIT'})},3000))});
		}
	}

  render() {
	return (
		<View style={{flex: 1, flexDirection: 'column'}}>
		<Modal
              visible={this.state.modalVisible}
              animationType={'slide'}
              onRequestClose={() => this.closeModal()}
          >
               <TextInput
               	 placeholder="http://192.168.0.1:5000/"
    			onChangeText={(uri) => this.setState({uri})}
    			value={this.state.uri}
				/>
				<Button onPress={()=>this.closeModal()} title='Submit URI'/>
        </Modal>
	    <View style={{backgroundColor:this.state.colorDict[this.state.response] ,flex:1,justifyContent: 'center',alignItems: 'center'}}>
	  	    <TouchableOpacity   onPress={()=>Expo.Fingerprint.authenticateAsync().then(res=>this.onScan(res.success))}>
	  		  <Image
	  		  source={require('./assets/finger_print.png')}
	  		  />
	  		</TouchableOpacity>
	  	</View>
	  	<View style={{height: 50, backgroundColor: 'powderblue'}} />
		</View>
	);
	}
}
