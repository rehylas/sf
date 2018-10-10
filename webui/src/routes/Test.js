

import React, { Component } from 'react'
import { connect } from 'dva'
//import { Chart, Tooltip, Geom, Legend, Axis } from 'bizcharts';
import { Table, Divider, Tag,Button } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import TimelineChart from '../components/TimelineChart'
import { browserHistory } from 'react-router'

class Test extends Component {

    constructor(props) {
        super(props);
        this.state = {date: new Date(), datalist:[] };
    }

    componentDidMount() {
        console.log( "Test  DidMount " )  
        
  
    }

    handleClick= (e) => {
        console.log('click')
        this.props.history.push('/zfline/RU0', {"code":"rb"} )
        //this.setState({ size: e.target.value });
      }

    render() {

        let dateStr ='测试页面'
        let code ="RB0"
        return (
            <div className={styles.normal}>
                <span>{dateStr}</span>
                <TimelineChart zfcode={code}/>
                <Button onClick = { this.handleClick } >点击</Button>
              
            </div>
        )
    }
}

Test.propsTypes = {}

export default connect()(Test)
 