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
      this.state = {date: new Date(), datalist:[] };
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
            this.state.datalist = adata
            // var   gettype=Object.prototype.toString;
            // console.log("type:", gettype.call(  adata )   )
            //this.setState({ datalist: adata } );   
        }             
      })
  } 

  render() {
    console.log( 'timeline render ', this.props.zfcode )
    this.getdata( this.props.zfcode )

    let data = [ ];
    if( this.state.datalist ){
        data = this.state.datalist ;  
        data.forEach( (rec,index,arr)=>{
          rec.zf = rec.zf.toFixed(2)
         
        } )
    }

    const ds = new DataSet();
    const dv = ds.createView().source(data);
    dv.transform({
      type: "fold",
      fields: ["zf5", "zf"],
      // 展开字段集
      key: "city",
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
            color={"city"}
            shape={"smooth"}
          />
          <Geom
            type="point"
            position="date*zfval"
            size={4}
            shape={"circle"}
            color={"city"}
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

