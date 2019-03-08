

import React, { Component } from 'react'
import { connect } from 'dva'
import { Table, Divider, Tag } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import PotLine from '../components/PotLine'
 
class StockPot extends Component {
    constructor(props) {
        super(props); 
        this.state = { };
 
    }

    componentDidMount() {
        console.log( "StockPot DidMount " )
 
    }

    render() {
        console.log('render : ')
         
        return (
            <div className={styles.normal}>
            <PotLine />
                                                
            </div>
        )
    }
}

StockPot.propsTypes = {}

export default connect()(StockPot)
 