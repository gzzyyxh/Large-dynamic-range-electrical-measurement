#include"stm32f10x_conf.h"
#include"main.h"
#define DIN_H GPIO_SetBits(GPIOC,GPIO_Pin_5)
#define DIN_L GPIO_ResetBits(GPIOC,GPIO_Pin_5)
#define SCLK_H GPIO_SetBits(GPIOC,GPIO_Pin_6)
#define SCLK_L GPIO_ResetBits(GPIOC,GPIO_Pin_6)
#define CLR_H GPIO_SetBits(GPIOC,GPIO_Pin_8)
#define CLR_L GPIO_ResetBits(GPIOC,GPIO_Pin_8)
#define SYNC_H GPIO_SetBits(GPIOC,GPIO_Pin_9)
#define SYNC_L GPIO_ResetBits(GPIOC,GPIO_Pin_9)
#define LDAC_H GPIO_SetBits(GPIOC,GPIO_Pin_4)
#define LDAC_L GPIO_ResetBits(GPIOC,GPIO_Pin_4)


#define AD7606OS0_H GPIO_SetBits(GPIOC,GPIO_Pin_2)
#define AD7606OS0_L GPIO_ResetBits(GPIOC,GPIO_Pin_2)
#define AD7606OS1_H GPIO_SetBits(GPIOC,GPIO_Pin_3)
#define AD7606OS1_L GPIO_ResetBits(GPIOC,GPIO_Pin_3)
#define AD7606OS2_H GPIO_SetBits(GPIOB,GPIO_Pin_0)
#define AD7606OS2_L GPIO_ResetBits(GPIOB,GPIO_Pin_0)

#define AD7606_CONVST_A_H GPIO_SetBits(GPIOA,GPIO_Pin_4)
#define AD7606_CONVST_A_L GPIO_ResetBits(GPIOA,GPIO_Pin_4)
#define AD7606_CONVST_B_H GPIO_SetBits(GPIOA,GPIO_Pin_1)
#define AD7606_CONVST_B_L GPIO_ResetBits(GPIOA,GPIO_Pin_1)

#define AD7606_SCLK_H GPIO_SetBits(GPIOC,GPIO_Pin_10)
#define AD7606_SCLK_L GPIO_ResetBits(GPIOC,GPIO_Pin_10)
#define AD7606_RESET_H GPIO_SetBits(GPIOC,GPIO_Pin_11)
#define AD7606_RESET_L GPIO_ResetBits(GPIOC,GPIO_Pin_11)
#define AD7606_CS_H GPIO_SetBits(GPIOC,GPIO_Pin_12)
#define AD7606_CS_L GPIO_ResetBits(GPIOC,GPIO_Pin_12)

#define AD7606_BUSY GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_13)
#define AD7606_DOUTB GPIO_ReadInputDataBit(GPIOA,GPIO_Pin_14)
#define AD7606_DOUTA GPIO_ReadInputDataBit(GPIOB,GPIO_Pin_7)

void RCC_Configuration(void); 
void GPIO_Configuration(void);
void NVIC_Configuration(void); 
void Delay(vu32 nCount);
void ADC1_Configuration(void);
void DAC8562_WRITE(uint8_t cmd,uint16_t data);
void AD7606_SETOS(uint8_t osv);
void AD7606_RESET(void);
uint16_t ad7606_ReadBytes(void);
void AD7606_STARTCONV(void);
void TimeInit(void);
uint16_t test1,test2;//Waveform array subscript
uint16_t datatemp[8];//AD7606 data acquisition TEMP

int main(void) 
{ 

  RCC_Configuration();    
  GPIO_Configuration(); 
  NVIC_Configuration(); 
  TimeInit();//Timer Interrupts Update DAC Waveforms
  CLR_L;
  LDAC_H;
  DAC8562_WRITE(0x28,0x0001);//init DAC8562/3
  DAC8562_WRITE(0x20,0x0003);
  DAC8562_WRITE(0x38,0x0001);
  
  AD7606_SETOS(0X00);//200Kbps
  AD7606_RESET();
  AD7606_CONVST_A_H;
  AD7606_CONVST_B_H;
  test1=0;
  test2=100;

  while (1) 
  { 
    if(!AD7606_BUSY)
    {
      AD7606_CS_L;
      for(uint8_t i = 0;i < 8;i++)
      {
        datatemp[i]=ad7606_ReadBytes();//Read ADC data
        if(datatemp[i]>32767)
        {
          datatemp[i]-=32767;
        }
        else
        {
          datatemp[i]+=32767;
        }
      }
      AD7606_CS_H;
      AD7606_STARTCONV();
      while(AD7606_BUSY);
    }
  } 
} 



void TIM3_IRQHandler(void)
{
  if(TIM_GetITStatus(TIM3, TIM_IT_Update) == SET)
  {
    TIM_ClearITPendingBit(TIM3,TIM_IT_Update);
  }
  DAC8562_WRITE(0x18,sindata[test1]);//Updata DAC data
  DAC8562_WRITE(0x19,sindata[test2]);//Updata DAC data
  LDAC_L;
  Delay(0x01);
  LDAC_H;
  test1++;
  test2++;
  if(test1>314)test1=0;
  if(test2>314)test2=0;
}


void TimeInit(void)
{
  TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
  NVIC_InitTypeDef NVIC_InitStructure;
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3,ENABLE);
  TIM_ClearITPendingBit(TIM3,TIM_IT_Update);
  TIM_TimeBaseStructure.TIM_Period = 10;
  TIM_TimeBaseStructure.TIM_Prescaler = 3000;
  TIM_TimeBaseStructure.TIM_ClockDivision = TIM_CKD_DIV1;
  TIM_TimeBaseStructure.TIM_CounterMode = TIM_CounterMode_Up;
  TIM_TimeBaseInit(TIM3, & TIM_TimeBaseStructure);
  TIM_ITConfig(TIM3, TIM_IT_Update, ENABLE );
  TIM_Cmd(TIM3, ENABLE);
  NVIC_PriorityGroupConfig(NVIC_PriorityGroup_1);
  NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;
  NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0;
  NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;
  NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;
  NVIC_Init(&NVIC_InitStructure);
}




void DAC8562_WRITE(uint8_t cmd,uint16_t data)
{
  SYNC_H;
  Delay(0x01);
  SYNC_L;
  SCLK_L;
  for(uint8_t s=0;s<8;s++)
  {
    if((cmd&0x80)==0x80){DIN_H;}
    else{DIN_L;}
    Delay(0x01);
    SCLK_H;
    Delay(0x01);
    cmd<<=1;
    SCLK_L;
    Delay(0x01);
  }
  for(uint8_t s=0;s<16;s++)
  {
    if((data&0x8000)==0x8000){DIN_H;}
    else{DIN_L;}
    Delay(0x01);
    SCLK_H;
    Delay(0x01);
    data<<=1;
    SCLK_L;
    Delay(0x01);
  }
}

void AD7606_STARTCONV(void)
{
  AD7606_CONVST_A_L;
  AD7606_CONVST_B_L;
  Delay(0xF);
  AD7606_CONVST_A_H;
  AD7606_CONVST_B_H;
}

uint16_t ad7606_ReadBytes(void)
{
  uint16_t usData = 0;
  for (uint8_t i = 0; i < 16; i++)
  {
    AD7606_SCLK_L;
    usData = usData << 1;
    if(AD7606_DOUTA)
    {
      usData |= 0x0001;
    }
    AD7606_SCLK_H;
  }
  return usData;		
}

void AD7606_RESET(void)
{
  AD7606_RESET_H;
  Delay(0xFF);
  AD7606_RESET_L;
}

void AD7606_SETOS(uint8_t osv)
{
  switch(osv)
  {
  case 0://000  200Kbps
    AD7606OS0_L;
    AD7606OS1_L;
    AD7606OS2_L;
    break;
  case 1://001
    AD7606OS0_H;
    AD7606OS1_L;
    AD7606OS2_L;
    break;
  case 2://010
    AD7606OS0_L;
    AD7606OS1_H;
    AD7606OS2_L;
    break;
  case 3://011
    AD7606OS0_H;
    AD7606OS1_H;
    AD7606OS2_L;
    break;
  case 4://100
    AD7606OS0_L;
    AD7606OS1_L;
    AD7606OS2_H;
    break;
  case 5://101
    AD7606OS0_H;
    AD7606OS1_L;
    AD7606OS2_H;
    break;
  case 6://110
    AD7606OS0_L;
    AD7606OS1_H;
    AD7606OS2_H;
    break;
  }
}

void RCC_Configuration(void) 
{    
  ErrorStatus HSEStartUpStatus;
  RCC_DeInit(); 
  RCC_HSEConfig(RCC_HSE_ON); 
  HSEStartUpStatus = RCC_WaitForHSEStartUp(); 
  if(HSEStartUpStatus == SUCCESS) 
  { 
    FLASH_PrefetchBufferCmd(FLASH_PrefetchBuffer_Enable); 
    FLASH_SetLatency(FLASH_Latency_2); 
    RCC_HCLKConfig(RCC_SYSCLK_Div1);  
    RCC_PCLK2Config(RCC_HCLK_Div1);  
    RCC_PCLK1Config(RCC_HCLK_Div2); 
    RCC_PLLConfig(RCC_PLLSource_HSE_Div1, RCC_PLLMul_9); 
    RCC_PLLCmd(ENABLE); 
    while(RCC_GetFlagStatus(RCC_FLAG_PLLRDY) == RESET) { } 
    RCC_SYSCLKConfig(RCC_SYSCLKSource_PLLCLK); 
    while(RCC_GetSYSCLKSource() != 0x08) { } 
  } 
  RCC_AHBPeriphClockCmd(RCC_AHBPeriph_DMA2, ENABLE); 
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO | RCC_APB2Periph_GPIOA| RCC_APB2Periph_GPIOB| RCC_APB2Periph_GPIOC, ENABLE); 
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_DAC, ENABLE); 
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE); 
} 

void GPIO_Configuration(void) 
{ 
  GPIO_InitTypeDef GPIO_InitStructure; 
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7|GPIO_Pin_8|GPIO_Pin_9; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOC, &GPIO_InitStructure); 
  
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_2|GPIO_Pin_3|GPIO_Pin_10|GPIO_Pin_11|GPIO_Pin_12; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOC, &GPIO_InitStructure); 
  
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_0; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOB, &GPIO_InitStructure); 

  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_1|GPIO_Pin_4; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 
  GPIO_Init(GPIOA, &GPIO_InitStructure); 

  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_13|GPIO_Pin_14|GPIO_Pin_15; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING; 
  GPIO_Init(GPIOA, &GPIO_InitStructure); 
  
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_7; 
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; 
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING; 
  GPIO_Init(GPIOB, &GPIO_InitStructure); 
  
} 


void NVIC_Configuration(void) 
{ 
#ifdef  VECT_TAB_RAM   
  NVIC_SetVectorTable(NVIC_VectTab_RAM, 0x0);  
#else
  NVIC_SetVectorTable(NVIC_VectTab_FLASH, 0x0);    
#endif 
} 

void Delay(vu32 nCount) 
{ 
  for(; nCount != 0; nCount--); 
} 

#ifdef  DEBUG 
void assert_failed(u8* file, u32 line) 
{  
  while (1) { } 
} 
#endif 