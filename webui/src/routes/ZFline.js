

import React, { Component } from 'react'
import { connect } from 'dva'
//import { Chart, Tooltip, Geom, Legend, Axis } from 'bizcharts';
import { Table, Divider, Tag } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'


class ZFline extends Component {

    constructor(props) {
        super(props);
        this.state = {date: new Date(), datalist:[] };
    }

    componentDidMount() {
        console.log( "ZFline  DidMount " )  
        let code ="RU0"
        request('/future/zf/'+ code ).then(data => { 
            console.log("------------")
            console.log( data )  
            this.setState({ datalist: data.data } );
            
        })
    
    }


    render() {

        let dateStr ='振幅排名'

        const columns = [{
            title: '合约',
            dataIndex: 'code',
            key: 'code',
            render: text => <a href="javascript:;">{text}</a>,
          }, {
            title: '振幅',
            dataIndex: 'zf20',
            key: 'zf20',
          }, {
            title: 'K线',
            dataIndex: 'kline',
            key: 'kline',
            render: text => <a href="javascript:;">K线图</a>,
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
                <Table columns={columns} dataSource={data} />
            </div>
        )
    }
}

ZFline.propsTypes = {}

export default connect()(ZFline)
 