

import React, { Component } from 'react'
import { connect } from 'dva'
import { Table, Divider, Tag } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import MyFstchart2       from '../components/MyFstchart2'

class Fst extends Component {
    constructor(props) {
        super(props); 
        this.state = { };
 
    }

    componentDidMount() {
        console.log( "Fst DidMount " )
 
    }

    render() {
        console.log('render : ')
         
        return (
            <div className={styles.normal}>
                <MyFstchart2 />                                   
            </div>
        )
    }
}

Fst.propsTypes = {}

export default connect()(Fst)
 