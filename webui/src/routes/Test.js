

import React, { Component } from 'react'
import { connect } from 'dva'
//import { Chart, Tooltip, Geom, Legend, Axis } from 'bizcharts';
import { Table, Divider, Tag } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import TimelineChart from '../components/TimelineChart'

class Test extends Component {

    constructor(props) {
        super(props);
        this.state = {date: new Date(), datalist:[] };
    }

    componentDidMount() {
        console.log( "Test  DidMount " )  
        
  
    }


    render() {

        let dateStr ='测试页面'
        let zfcode ="RB0"
        return (
            <div className={styles.normal}>
                <span>{dateStr}</span>
                <TimelineChart code={zfcode}/>
              
            </div>
        )
    }
}

Test.propsTypes = {}

export default connect()(Test)
 