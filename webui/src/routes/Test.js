

import React, { Component } from 'react'
import { connect } from 'dva'
//import { Chart, Tooltip, Geom, Legend, Axis } from 'bizcharts';
import { Table, Divider, Tag,Button } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import TimelineChart from '../components/TimelineChart'
import Mychart       from '../components/Mychart'
import MyKchart       from '../components/MyKchart'
import MyKchart2       from '../components/MyKchart2'
import MyFstchart       from '../components/MyFstchart'
import EchartsTest       from '../components/EchartsTest'

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
        let code ="RU0"
        return (
            <div className={styles.normal}>

                {/* <span>{dateStr}</span>
                <TimelineChart zfcode={code}/>
                <Button onClick = { this.handleClick } >点击</Button>
                <span> 图表使用 </span>
                <Mychart /> */}
                {/* <MyKchart code={code}/> */}

                <EchartsTest/>

                {/* <MyKchart2/> */}

                <MyFstchart/>
              
            </div>
        )
    }
}

Test.propsTypes = {}

export default connect()(Test)
 