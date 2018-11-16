

import React, { Component } from 'react'
import { connect } from 'dva'
import { Table, Divider, Tag } from 'antd';

import styles from './Top5.css'
import request from '../utils/request'
import TimelineChart from '../components/TimelineChart'
import MyKchart2       from '../components/MyKchart2'

class Top5 extends Component {

    constructor(props) {
        super(props); 
        this.state = {date: new Date(), datalist:[], code :'RU0' };

        // this.handleClickCode = this.handleClickCode.bind( this );

    }

    componentDidMount() {
        console.log( "Top5 DidMount " )
        request('/future/zf_top5').then(data => { 
            console.log("------------")
            console.log( data )  
            this.setState({ datalist: data.data } );
            
        })
         
        console.log("params:", this.props.match)
    
    }

     

    // handleClickCode(txt,a,b) {
    //     console.log('The link was clicked.  '  );
    //     console.log( txt.val   );
  

    //     //txt.preventDefault();
 
    //     // this.setState({
    //     //     Val: 100
    //     // });
    // }

  

    render() {

        let dateStr ='振幅排名'

        const columns = [{
            title: '合约',
            dataIndex: 'code', //{ this.handleClickCode } 
            key: 'code',
            render: text =>  <a href="javascript:void(0);" onClick=  {this.handleClickCode} >{text}</a>,
          }, {
            title: '振幅',
            dataIndex: 'zf20',
            key: 'zf20',
          }
        //   , {
        //     title: 'K线',
        //     dataIndex: 'kline',
        //     key: 'kline',
        //     render: text => <a href="javascript:;">K线图</a>,
        //   }

        ];
     
         let data = []
         if( this.state.datalist )
            data = this.state.datalist.data  
         //let code = this.state.code 
         console.log('render : ')
         console.log( data )
        return (
            <div className={styles.normal}>
                <span>{dateStr}</span>
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
                <span>{ this.state.code }   振幅曲线</span>
                <TimelineChart zfcode={ this.state.code  } />

                <span>{ this.state.code }   k线图</span>
                <MyKchart2  code={ this.state.code  } />                  
            </div>
        )
    }
}

Top5.propsTypes = {}

export default connect()(Top5)
 