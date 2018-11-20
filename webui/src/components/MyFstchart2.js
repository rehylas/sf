

import React, { Component } from 'react'
import { connect } from 'dva'
import { Calendar, Row, Col, Tree, Icon } from 'antd';

import MyFstchart from '../components/MyFstchart'
//import { browserHistory } from 'react-router'

const TreeNode = Tree.TreeNode;

class MyFstchart2 extends Component {

    constructor(props) {
        super(props);
        this.state = { date: new Date(), datalist: [] , fstDate : '2018-11-20' };
    }

    componentDidMount() {
        console.log("MyFstchart2  DidMount ")


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
        let symbols =['RU','RB','TA','ZN','FU','J','M','L']
        return (
            <div  >
                <Row  >
                <Col span={19} > <MyFstchart code= {this.state.code}    date =  {this.state.fstDate} /> </Col>
                <Col span={1}  >
                    <br/><br/>
                    <div style={{ width: 300, border: '1px solid #d9d9d9', borderRadius: 4 }}>
                        <Calendar fullscreen={false} onSelect={this.onSelect}  onPanelChange={this.onPanelChange} />
                    </div>     
                    <div>
                    <Tree  onSelect={ this.onSelectCode }   >
                        <TreeNode icon={<Icon type="smile-o" />} title="品种" key="0-0">
                            {    
                                symbols.map((item, index) => {
                                    console.log('item:', item )
                                    return ( <TreeNode icon={<Icon type="right" />} title={ item } key={item+'0'} /> )
                                })
                            }


                            {/* <TreeNode icon={<Icon type="meh-o" />} title="RU" key="RU0" />
                            <TreeNode
                                icon={({ selected }) => (
                                <Icon type={selected ? 'frown' : 'frown-o'} />
                                )}
                                title="RB"
                                key="RB0"
                            /> */}
                        </TreeNode>
                    </Tree>
                    </div>           
                </Col>
 
                </Row>

            </div>
        )
    }
}

MyFstchart2.propsTypes = {}

export default connect()(MyFstchart2)

