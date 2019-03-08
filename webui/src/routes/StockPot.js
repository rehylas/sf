

import React, { Component } from 'react'
import { connect } from 'dva'
import { Table, Divider, Tag } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import PotLine from '../components/PotLine'
 
class StockPot extends Component {
    constructor(props) {
        super(props); 
        this.state = {  code:'002415' };
 
    }

    componentDidMount() {
        console.log( "StockPot DidMount ", this.props.match.params.code )
        this.state.code = this.props.match.params.code
        this.setState({ code: this.state.code })
 

    }

    render() {
        console.log('StockPot render : ',  this.props.match.params.code )
         
        return (
            <div className={styles.normal}>
            <PotLine code={ this.props.match.params.code} />
                                                
            </div>
        )
    }
}

StockPot.propsTypes = {    }

export default connect()(StockPot)
 