import React from "react";
import {
  G2,
  Chart,
  Geom,
  Axis,
  Tooltip,
  Coord,
  Label,
  Legend,
  View,
  Guide,
  Shape,
  Facet,
  Util
} from "bizcharts";
import DataSet from "@antv/data-set";
import request from '../utils/request'


class TimelineChart extends React.Component { //_ZF 

  constructor(props) {
      super(props);
      this.state = {date: new Date(), datalist:[], updateState:false };
  }

  componentDidMount() {
      console.log( "TimelineChart DidMount " )
      this.getdata( this.props.zfcode )
 

  }

  getdata = ( code )=>{
      let dataUrl = '/future/zf/' + this.props.zfcode 
      console.log( dataUrl )    
      request( dataUrl ).then(data => { 
        
        console.log('request : '+ dataUrl  +'  '+ this.props.zfcode )
        if( data.data ){  
          
            let adata = data.data.data 
            console.log('request : ' + adata.length   )
            console.log( adata[0] )

            adata.forEach( (rec,index,arr)=>{
 
              rec.zf = rec.zf.toFixed(2)
             
            } )

            this.state.datalist = adata
            this.state.updateState  = true 
            this.setState({ datalist: adata } ); 
   
        }             
      })
  } 

  render() {
    console.log( 'timeline render ', this.props.zfcode )
    

    if( this.state.updateState  == true ){
      this.state.updateState  = false
    }else{
      this.getdata( this.props.zfcode )
    }    

 
    const ds = new DataSet();
    const dv = ds.createView().source( this.state.datalist );
    dv.transform({
      type: "fold",
      fields: ["zf5", "zf"],
      // 展开字段集
      key: "blue",//["zf5", "zf"]  ,
      // key字段
      value: "zfval" // value字段
    });
    console.log(dv);
    const cols = {
      date: {
        type: 'timeCat',
        range: [0, 1]
      }
    };
    return (
      <div>
        <Chart height={400} data={dv} scale={cols} forceFit>
          <Legend />
          <Axis name="date" />
          <Axis
            name="zfval"
            label={{
              formatter: val => `${val}`
            }}
          />
          <Tooltip
            crosshairs={{
              type: "y"
            }}
          />
          <Geom
            type="line"
            position="date*zfval"
            size={2}
            color={"blue"}
            shape={"smooth"}
          />
          <Geom
            type="line"
            position="date*zfval"
            size={4}
            shape={"circle"}
            color={"blue"}
            style={{
              stroke: "#fff",
              lineWidth: 1
            }}
          />
        </Chart>
      </div>
    );
  }
}

TimelineChart.defaultProps = {
  zfcode: 'RU0'
}

export default TimelineChart;

