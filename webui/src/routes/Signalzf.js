

import React, { Component } from 'react'
import { connect } from 'dva'
import { Table, Divider, Tag , Row, Col } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import TimelineChart from '../components/TimelineChart'
import MyKchart2       from '../components/MyKchart2'
import MyFstchart       from '../components/MyFstchart'


class Signalzf extends Component {

    constructor(props) {
        super(props);
        this.state = {date: new Date(), datalist:[],code:'RU0' };
    }

    componentDidMount() {
        console.log( "Signalzf DidMount " )
        request('/future/signal_in_zf_top5').then(data => { 
            console.log("------------")
            console.log( data )  
            this.setState({ datalist: data.data } );
            
        })
    
    }

    render() {

        let dateStr ='振幅进前5信号'

        const columns = [{
            title: '合约',
            dataIndex: 'code',
            key: 'code',
            render: text => <a href="javascript:;">{text}</a>,
          }, 
          // {
          //   title: '振幅',
          //   dataIndex: 'zf20',
          //   key: 'zf20',
          // }, 
          // {
          //   title: 'K线',
          //   dataIndex: 'kline',
          //   key: 'kline',
          //   render: text => <a href="javascript:;">K线图</a>,
          // }, 
          {
            title: '日期',
            dataIndex: 'date',
            key: 'date',
             
          }
          
        //   , {
        //     title: 'Tags',
        //     key: 'tags',
        //     dataIndex: 'tags',
        //     render: tags => (
        //       <span>
        //         {tags.map(tag => <Tag color="blue" key={tag}>{tag}</Tag>)}
        //       </span>
        //     ),
        //   }, {
        //     title: 'Action',
        //     key: 'action',
        //     render: (text, record) => (
        //       <span>
        //         <a href="javascript:;">Invite {record.name}</a>
        //         <Divider type="vertical" />
        //         <a href="javascript:;">Delete</a>
        //       </span>
        //     ),
        //   }
        
        ];
          /*
          const data = [{
            key: '1',
            name: 'RU',
            zf: 3.5,
            kline: 'New York No. 1 Lake Park',
            tags: ['nice', 'developer'],
          }, {
            key: '2',
            name: 'TA',
            zf: 3.3,
            kline: 'London No. 1 Lake Park',
            tags: ['loser'],
          }, {
            key: '3',
            name: 'RB',
            zf: 3.1,
            kline: 'Sidney No. 1 Lake Park',
            tags: ['cool', 'teacher'],
          }];
          */
         let data = []
         if( this.state.datalist )
            data = this.state.datalist.data   
         console.log('render : ')
         console.log( data )
        return (
            <div className={styles.normal}>
                <span>{dateStr}</span>
                <Row  >  
                <Col span={8} > 
                    <Table columns={columns} dataSource={data} 
                                    onRow={(record) => {
                                        return {
                                            onClick: () => {  // 点击行
                                                console.log('onRow onClick:', record )
                                                // code = record.code 
                                                // this.props.history.push('/zfline/' + record.code )
                                                this.setState(  { code: record.code  }  )
                                            },       
                                        
                                        
                                        };
                                    }}
                    />
                </Col>    
                <Col span={16} > 
                {/* <span>{ this.state.code }   振幅曲线</span> */}
                <TimelineChart zfcode={ this.state.code  } />   
                
                </Col>   
                </Row>
                {/* <span>{ this.state.code }   k线图</span> */}
                <MyKchart2  code={ this.state.code  } /> 

                {/* <span>  分时图</span> */}
                <MyFstchart  code={ this.state.code   }  />   

            </div>
        )
    }
}

Signalzf.propsTypes = {}

export default connect()(Signalzf)
 