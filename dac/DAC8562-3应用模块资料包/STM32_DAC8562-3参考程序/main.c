#include"stm32f10x_conf.h"


#define DIN_H GPIO_SetBits(GPIOC,GPIO_Pin_0)
#define DIN_L GPIO_ResetBits(GPIOC,GPIO_Pin_0)
#define SCLK_H GPIO_SetBits(GPIOC,GPIO_Pin_1)
#define SCLK_L GPIO_ResetBits(GPIOC,GPIO_Pin_1)
#define CLR_H GPIO_SetBits(GPIOC,GPIO_Pin_2)
#define CLR_L GPIO_ResetBits(GPIOC,GPIO_Pin_2)
#define SYNC_H GPIO_SetBits(GPIOC,GPIO_Pin_3)
#define SYNC_L GPIO_ResetBits(GPIOC,GPIO_Pin_3)
#define LDAC_H GPIO_SetBits(GPIOC,GPIO_Pin_4)
#define LDAC_L GPIO_ResetBits(GPIOC,GPIO_Pin_4)

void RCC_Configuration(void);
void GPIO_Configuration(void);
void NVIC_Configuration(void);
void Delay(vu32 nCount);
void ADC1_Configuration(void);
void DAC8562_WRITE(uint8_t cmd,uint16_t data);

int main(void)
{

  RCC_Configuration();
  GPIO_Configuration();
  NVIC_Configuration();
  CLR_L;
  LDAC_H;
  DAC8562_WRITE(0x28,0x0001);
  DAC8562_WRITE(0x20,0x0003);
  DAC8562_WRITE(0x38,0x0001);

  uint16_t test;

  while (1)
  {
    DAC8562_WRITE(0x18,test);
    DAC8562_WRITE(0x19,test);
    LDAC_L;
    Delay(0x01);
    LDAC_H;
    test+=200;
  }
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
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO | RCC_APB2Periph_GPIOC, ENABLE);
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_DAC, ENABLE);
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM6, ENABLE);
}

void GPIO_Configuration(void)
{
  GPIO_InitTypeDef GPIO_InitStructure;
  GPIO_InitStructure.GPIO_Pin =  GPIO_Pin_0|GPIO_Pin_1|GPIO_Pin_2|GPIO_Pin_3|GPIO_Pin_4;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
  GPIO_Init(GPIOC, &GPIO_InitStructure);
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