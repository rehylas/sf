

import React, { Component } from 'react'
import { connect } from 'dva'
//import { Chart, Tooltip, Geom, Legend, Axis } from 'bizcharts';
import { Table, Divider, Tag, Button, Calendar, Row, Col, Tree, Icon } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import TimelineChart from '../components/TimelineChart'
import Mychart from '../components/Mychart'
import MyKchart from '../components/MyKchart'
import MyKchart2 from '../components/MyKchart2'
import MyFstchart2 from '../components/MyFstchart2'
import EchartsTest from '../components/EchartsTest'
import EchartsTest2 from '../components/EchartsTest2'
import {testFun} from '../utils/comm'

import { browserHistory } from 'react-router'

//var api_cxp = require('./cxpAPI');

const TreeNode = Tree.TreeNode;



class Test extends Component {

    constructor(props) {
        super(props);
        this.state = { date: new Date(), datalist: [] , fstDate : '2018-11-20' };
    }

    componentDidMount() {
        console.log("Test  DidMount ")
        testFun()


    }

    handleClick = (e) => {
        console.log('click')
        this.props.history.push('/zfline/RU0', { "code": "rb" })
        //this.setState({ size: e.target.value });
    }

    onPanelChange  = (value, mode) => {
        console.log(value, mode);
    }
     
    onSelect  = (value ) => {
        console.log(value.format("YYYY-MM-DD")  );
        //this.state.date = '2018-11-20';
        this.setState( {fstDate: value.format("YYYY-MM-DD")} )
        
    }

    onSelectCode  = ( selectKeys, e) =>{
        console.log( 'onSelectCode:', selectKeys  );  
        if( selectKeys.length  > 0 ){
            let keyVal = selectKeys[0]
            this.setState( {code: keyVal } )

            console.log( 'onSelectCode:', selectKeys  );   
            //console.log( 'onSelectCode:', e.node.key  );   
        }            
    }

    //function(selectedKeys, e:{selected: bool, selectedNodes, node, event})

    render() {

        let dateStr = '测试页面'
        let code = "RU0"
        return (
            <div className={styles.normal}>

                {/* <span>{dateStr}</span>
                <TimelineChart zfcode={code}/>
                <Button onClick = { this.handleClick } >点击</Button>
                <span> 图表使用 </span>
                <Mychart /> */}
                {/* <MyKchart code={code}/> */}

                <EchartsTest />
                <EchartsTest2 />

                {/* <MyKchart2/> */}

                <MyFstchart2/>
                

                {/* <Row  >
               
                <Col span={19} > <MyFstchart code= {this.state.code}     /> </Col>  
                <Col span={1}  >
                    <br/><br/>
                    <div style={{ width: 300, border: '1px solid #d9d9d9', borderRadius: 4 }}>
                        <Calendar fullscreen={false} onSelect={this.onSelect}  onPanelChange={this.onPanelChange} />
                    </div>     
                    <div>
                    <Tree  onSelect={ this.onSelectCode }   >
                        <TreeNode icon={<Icon type="smile-o" />} title="品种" key="0-0">
                            <TreeNode icon={<Icon type="meh-o" />} title="RU" key="RU0" />
                            <TreeNode
                                icon={({ selected }) => (
                                <Icon type={selected ? 'frown' : 'frown-o'} />
                                )}
                                title="RB"
                                key="RB0"
                            />
                        </TreeNode>
                    </Tree>
                    </div>           
                </Col>
 
                </Row> */}


                


            </div>
        )
    }
}

Test.propsTypes = {}

export default connect()(Test)

